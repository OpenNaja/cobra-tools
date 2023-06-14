import json
import os
import time
import sys
from pkgutil import iter_modules
from importlib import import_module
from root_path import root_dir

dict_names = ("hashes", "mimes", "shaders")

# 3.10 has and issue with large dict files, regression fixed in 3.11
ver = sys.version_info
if ver.major == 3 and ver.minor == 10:
	raise Exception('Python 3.10 is not supported, please upgrade to 3.11 at least.')


class ConstantsProvider(dict):

	def __init__(self):
		super().__init__()

		# iterate through the modules in the current package
		package_dir = os.path.join(root_dir, "constants")
		for game in os.listdir(package_dir):
			game_dir = os.path.join(package_dir, game)
			# ignore that
			if "pycache" in game:
				continue
			if os.path.isdir(game_dir):
				self[game] = {}
				for dict_name in dict_names:
					self[game][dict_name] = {}
				for (_, module_name, _) in iter_modules([game_dir]):
					# import the module and iterate through its attributes
					module = import_module(f"constants.{game}.{module_name}")
					for dict_name in dict_names:
						# make sure the right variable is accessed
						if dict_name in module_name:
							# update the dict so we can easily have custom additions
							self[game][dict_name].update(getattr(module, dict_name))

	@property
	def extractables(self):
		return [ext for ext, loader in self.items() if loader.can_extract]

	@property
	def ignore_types(self):
		return [ext for ext, loader in self.items() if not loader.can_extract]


if __name__ == '__main__':
	# start = time.time()
	# cp = ConstantsProvider()
	# dur = time.time()-start
	# print(dur)

	start = time.time()
	module = import_module(f"constants.Jurassic World Evolution 2.hashes")
	dur = time.time() - start
	print(dur)

	start = time.time()
	with open(os.path.join(root_dir, "constants", "Jurassic World Evolution 2", "hashes.json"), "r") as json_reader:
		a = json.load(json_reader)
		print(a["10236475"])
	dur = time.time() - start
	print(dur)
	# print(cp)
