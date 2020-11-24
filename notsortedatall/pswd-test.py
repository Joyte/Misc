import base64,subprocess,sys,os

# define our clear function 
def clearscreen(): 
  
	# for windows 
	if os.name == 'nt': 
		os.system('cls') 
  
	# for mac and linux(here, os.name is 'posix') 
	else: 
		os.system('clear') 

clearscreen()

try:
	from cryptography.hazmat.backends import default_backend
	from cryptography.hazmat.primitives import hashes
	from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
	from cryptography.fernet import Fernet
except ModuleNotFoundError:
	subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
	from cryptography.hazmat.backends import default_backend
	from cryptography.hazmat.primitives import hashes
	from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
	from cryptography.fernet import Fernet
	clearscreen()


#Password codex
password = input("Password: ")
password = password.encode()
salt = b'ofog2t93rw74teryugfdhft47i657itagd95q36rtwy'

kdf = PBKDF2HMAC(
	algorithm=hashes.SHA256(),
	length=32,
	salt=salt,
	iterations=100000,
	backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)

print(f"key = {key}")

encrypted = f.encrypt(password)

print(f"encrypted = {encrypted}")

decrypted = f.decrypt(encrypted).decode("utf-8")

print(f"decrypted = {decrypted}")

input("exit")