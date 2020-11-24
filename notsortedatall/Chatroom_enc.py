import socket,errno,select,sys,base64,subprocess,os
from cryptography.fernet import Fernet

#Options
HEADER_LENGTH = 10
IP = "139.99.135.176"
PORT = 63234




# define our clear function 
def clearscreen(): 
	# for windows 
	if os.name == 'nt': 
		_ = os.system('cls') 
	# for mac and linux(here, os.name is 'posix') 
	else: 
		_ = os.system('clear') 
clearscreen()

try:
	from cryptography.hazmat.backends import default_backend
	from cryptography.hazmat.primitives import hashes
	from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
	from cryptography.fernet import Fernet
except ModuleNotFoundError:
	print("Installing cryptography package...")
	subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
	from cryptography.hazmat.backends import default_backend
	from cryptography.hazmat.primitives import hashes
	from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
	from cryptography.fernet import Fernet
	clearscreen()

#Username
firstreq=True
while 1:
	if firstreq == False: print("That's not a valid username, please use only alphabetical characters!\n")
	firstreq=False
	my_username = input("Username: ")
	if not my_username.isalpha():
		pass
	else:
		del firstreq
		break

#Password code
password = input("Password: ")
password = password.encode()

kdf = PBKDF2HMAC(
	algorithm=hashes.SHA256(),
	length=32,
	salt=b'ofog2t93rw74teryugfdhft47i657itagd95q36rtwy',
	iterations=100000,
	backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))
keymanager = Fernet(key)

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	# Connect to a given ip and port
	client_socket.connect((IP, PORT))
except ConnectionRefusedError: 
	#If the server is not running, tell the user so.
	input("The server is down, please check back again later!\n\nPress enter to exit...")
	sys.exit()

# Set connection to non-blocking state, so .recv() call won't block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')

tosend_encrypted = keymanager.encrypt(username_header + username)
client_socket.send(tosend_encrypted)

while True:

	# Wait for user to input a message
	message = input(f'{my_username} > ')

	# If message is not empty - send it
	if message.strip() == "":
		# Encode message to bytes, prepare header and convert to bytes, like for username above, then send
		message = message.encode('utf-8')
		message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
		tosend_encrypted = keymanager.encrypt(bytes(message_header) + bytes(username))
		client_socket.send(tosend_encrypted)
	else:
		print("Your message is empty!")



	try:
		# Now we want to loop over received messages (there might be more than one) and print them
		while True:

			# Receive our "header" containing username length, it's size is defined and constant
			username_header = client_socket.recv(HEADER_LENGTH)
			try:
				username_header = keymanager.decrypt(username_header)
			except InvalidToken:
				input("Your key is invalid!\n\nPress enter to exit...")
				sys.exit()

			# If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
			if not len(username_header):
				print('Connection closed by the server')
				sys.exit()

			# Convert header to int value
			username_length = int(username_header.decode('utf-8').strip())

			# Receive and decode username
			username = client_socket.recv(username_length).decode('utf-8')

			# Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
			message_header = client_socket.recv(HEADER_LENGTH)
			try:
				username_header = keymanager.decrypt(username_header)
			except InvalidToken:
				input("Your key is invalid!\n\nPress enter to exit...")
				sys.exit()

			message_length = int(message_header.decode('utf-8').strip())
			message = client_socket.recv(message_length)
			try:
				message = keymanager.decrypt(message).decode('utf-8')
			except InvalidToken:
				input("Your key is invalid!\n\nPress enter to exit...")
				sys.exit()

			# Print message
			print(f'{username} > {message}')

	except IOError as e:
		# This is normal on non blocking connections - when there are no incoming data error is going to be raised
		# Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
		# We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
		# If we got different error code - something happened
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print('Reading error: {}'.format(str(e)))
			sys.exit()

		# We just did not receive anything
		continue

	except Exception as e:
		# Any other exception - something happened, exit
		print('Reading error: '.format(str(e)))
		sys.exit()