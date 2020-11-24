def check(txt1 : str, txt2 : str):
	notit = []
	if len(txt1) != len(txt2):
		if len(txt1) > len(txt2):
			return (len(txt1) - len(txt2), txt1[:-len(txt2)])
		else:
			return (len(txt2) - len(txt1), txt2[:-len(txt1)])



	for t1, t2 in zip(txt1, txt2):
		if t1 != t2:
			notit.append((num, t1, t2))

	if notit != []:
		return notit
	else:
		return True




print(check(". -.. .- -... -... .. -   -.-. .... .- .-.. .-.. . -. --.", ". -.. .- -... -... .. -   -.-. .... .- .-.. .-.. . -. --. ."))