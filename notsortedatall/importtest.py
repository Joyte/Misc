
exec("import abc")

def import_os():
	exec("import os", globals())

import_os()

print(abc)
print(os)