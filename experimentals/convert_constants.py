import json
import os
from pkgutil import iter_modules
from importlib import import_module
import logging

from ovl_util.mimes import Mime
from root_path import root_dir
strs = ("mimes_name", "mimes_mime_hash", "mimes_mime_version", "mimes_triplet_count", "mimes_triplets", "files_pool_type", "files_set_pool_type")
ignores = ("triplet_count", )
game_lut = {'DLA': 'Disneyland Adventures', 'JWE': 'Jurassic World Evolution', 'JWE2': 'Jurassic World Evolution 2', 'PC': 'Planet Coaster', 'PZ': 'Planet Zoo', 'ZTUAC': 'Zoo Tycoon Ultimate Animal Collection'
}


class ConstantsConverter:

	def __init__(self):
		# iterate through the modules in the current package
		package_dir = os.path.join(root_dir, "hashes")
		# print(package_dir)
		for (_, module_name, _) in iter_modules([package_dir]):
			try:
				game = module_name.split("_")[-1].upper()
				game = game_lut[game]
				# create output path
				out_dir = os.path.join(root_dir, "constants", game)
				os.makedirs(out_dir, exist_ok=True)
				# process mimes
				if "constants_" in module_name:
					# import the module and iterate through its attributes
					module = import_module(f"hashes.{module_name}")
					dicts = {}
					for attribute_name in dir(module):
						if attribute_name in strs:
							attribute = getattr(module, attribute_name)
							assert type(attribute) == dict
							dicts[attribute_name] = attribute
					# get list of formats used in all dicts
					formats = list(sorted(set().union(*(d.keys() for d in dicts.values()))))
					# print(formats)
					out_fp = os.path.join(out_dir, f"mimes.py")
					# populate mimes classes and write file
					with open(out_fp, "w") as f:
						f.write(f"from ovl_util.mimes import Mime\n\n")
						dic = {}
						for format_name in formats:
							mime = Mime("", 0, 0, [], 0, 0)
							for var in strs:
								val = dicts[var][format_name]
								short_var = var.replace("mime_", "").replace("mimes_", "").replace("files_", "").replace("_type", "")
								if short_var in ignores:
									continue
								setattr(mime, short_var, val)
							# f.write(str(mime))
							# f.write("\n")
							dic[mime.ext] = mime
						f.write(f"mimes = {dic}\n")

			except ModuleNotFoundError:
				logging.exception(f"Could not load {module_name}")

		hashes_dir = os.path.join(root_dir, "hashes")
		for file in os.listdir(hashes_dir):
			hash_table_global = {}
			fp = os.path.join(hashes_dir, file)
			if fp.endswith(".txt"):
				game = os.path.splitext(file)[0].split("-")[-1].upper()
				game = game_lut[game]
				# create output path
				out_dir = os.path.join(root_dir, "constants", game)
				os.makedirs(out_dir, exist_ok=True)
				with open(fp, "r") as f:
					for line in f:
						line = line.strip()
						if line:
							k, v = line.split(" = ")
							hash_table_global[int(k)] = v

				# with open(os.path.join(out_dir, "hashes.json"), "w") as json_writer:
				# 	json.dump(hash_table_global, json_writer, indent="\t", sort_keys=True)

				with open(os.path.join(out_dir, "hashes.py"), "w") as f:
					f.write(f"hashes = {hash_table_global}\n")


if __name__ == '__main__':
	ConstantsConverter()
