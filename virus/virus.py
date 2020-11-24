import os
for file in os.listdir():
	continue  # This is here for safety reasons, only remove it if you're serious about deleting everything in the same directory!
	with open("./{}".format(file), "w+") as fp:
		print("Erased '{}'".format(file))