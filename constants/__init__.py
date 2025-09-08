import json
import logging
import os
import time
import sys
from pkgutil import iter_modules
from importlib import import_module
from dataclasses import dataclass

dict_names = ("audio", "hashes", "mimes", "shaders", "textures", "texchannels")

# 3.10 has an issue with large dict files, regression fixed in 3.11
try:
	import bpy
except:
	ver = sys.version_info
	if ver.major == 3 and ver.minor == 10:
		raise Exception('Python 3.10 is not supported, please upgrade to 3.11 at least.')


# @dataclass(init=False, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, )
@dataclass
class Mime:
	name: str
	hash: int
	version: int
	triplets: list
	pool: int
	set_pool: int = 0

	@property
	def class_name(self):
		return self.name.split(":")[1]

	@property
	def ext(self):
		return f".{self.name.split(':')[2]}"


@dataclass
class Shader:
	# name: str
	textures: set
	attributes: dict

	# @property
	# def class_name(self):
	# 	return self.name.split(":")[1]
	#
	# @property
	# def ext(self):
	# 	return f".{self.name.split(':')[2]}"


class ConstantsProvider(dict):

	def __init__(self, only_types=()):
		super().__init__()

		# iterate through the modules in the current package
		package_dir = os.path.dirname(__file__)
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
					# skip import of unwanted modules
					if only_types and module_name not in only_types:
						continue
					try:
						# import the module and iterate through its attributes
						module = import_module(f"constants.{game}.{module_name}")
						for dict_name in dict_names:
							# make sure the right variable is accessed
							if dict_name in module_name:
								# update the dict so we can easily have custom additions
								self[game][dict_name].update(getattr(module, dict_name))
					except OverflowError:
						logging.warning(f"Can't import 'constants.{game}.{module_name}' due to overflow error (py 3.10)")

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
	with open(os.path.join(os.path.dirname(__file__), "Jurassic World Evolution 2", "hashes.json"), "r") as json_reader:
		a = json.load(json_reader)
		print(a["10236475"])
	dur = time.time() - start
	print(dur)
	# print(cp)
