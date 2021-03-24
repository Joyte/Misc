import re
encoding="utf-8"  # Change this if you're using it with a different encoding
filename = input("File: ")
with open(f"./{filename}", "r", encoding=encoding) as fp:
	file = fp.read()
	newfile = ""
	replace = False
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

	with open(f"./{filename}-exec.py", "w", encoding=encoding) as fp2:
		fp2.write(f"exec(\"{newfile}\", dict(globals(), **locals()))")

	print("Turned file into exec")
