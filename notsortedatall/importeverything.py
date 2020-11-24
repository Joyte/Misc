BLACKLIST = ["antigravity", "formatter", "imp", "__phello__.foo", "this", "macpath"]
from distutils.sysconfig import get_python_lib
from os import listdir
from sys import builtin_module_names
for package in listdir(get_python_lib()[:-13]):
	if package.endswith(".py"):
		package = package[:-3]
		if package in BLACKLIST:
			continue

		try:
			exec("import " + package, globals())
		except ModuleNotFoundError:
			pass
for package in builtin_module_names:
	exec("import " + package, globals())





print(sys,abc,datetime)