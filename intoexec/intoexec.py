import re
filename = input("File: ")
with open(f"./{filename}", "r") as fp:
	file = fp.read()
	newfile = ""
	replace = False
	lastchar = ""
	for char in file:
		if char == "\t":
			newfile += "\\t"
			replace = True

		if char == "\n":
			newfile += "\\n"
			replace = True

		if char == "\"":
			newfile += "\\\""
			replace = True

		if char == "\\":
			newfile += "\\\\"
			replace	= True

		if not replace:
			newfile += char

		replace = False
		lastchar = char

	with open(f"./{filename}-exec.py", "w") as fp2:
		fp2.write(f"exec(\"{newfile}\", globals())")

	print("Turned file into exec")