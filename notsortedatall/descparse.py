desc = """
<@222832010106765312>,
	Bump done :thumbsup:
	Check it on DISBOARD: https://disboard.org/
"""



import re

def stringPOP(string, position):
	string = list(string)
	string.pop(position)
	return "".join(string)

def get_id_bump(description):
	match = re.search(r"<@!?[0-9]{18}?>", description)
	if match is None:
		return

	match = stringPOP(match.group(0), 0)
	match = stringPOP(match, 0)
	if match[0] == "!":
		match = stringPOP(match, 0)
	match = stringPOP(match, len(match)-1)
	
	return match



print(get_id_bump(desc))