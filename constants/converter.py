import json
import os
from pkgutil import iter_modules
from importlib import import_module
import logging

from constants import Mime

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
strs = ("mimes_name", "mimes_mime_hash", "mimes_mime_version", "mimes_triplet_count", "mimes_triplets", "files_pool_type", "files_set_pool_type")
ignores = ("triplet_count", )
game_lut = {'DLA': 'Disneyland Adventures', 'JWE': 'Jurassic World Evolution', 'JWE2': 'Jurassic World Evolution 2', 'PC': 'Planet Coaster', 'PZ': 'Planet Zoo', 'ZTUAC': 'Zoo Tycoon'
}


def write_formatted_dict(f, d, key=None):
	f.write("{\n")
	f.write(",\n".join(f"\t\"{k}\": {v}" for k, v in sorted(d.items(), key=key)))
	f.write("\n}\n")


def write_hashes_dict(out_fp, hashes):
	with open(out_fp, "w") as f:
		f.write("hashes = {\n")
		f.write(",\n".join(f"\t{k}: \"{v}\"" for k, v in sorted(hashes.items(), key=lambda item: item[1])))
		f.write("\n}\n")


def write_audio_dict(out_fp, audio):
	with open(out_fp, "w") as f:
		f.write("audio = {\n")
		f.write(",\n".join(f"\t{k}: \"{v}\"" for k, v in sorted(audio.items(), key=lambda item: item[1])))
		f.write("\n}\n")


def write_mimes_dict(out_fp, mimes):
	with open(out_fp, "w") as f:
		f.write(f"from constants import Mime\n\n")
		f.write("mimes = {\n")
		# for np 2.0, cast scalars to str manually
		f.write(",\n".join(f"\t\"{k}\": {str(v)}" for k, v in sorted(mimes.items())))
		f.write("\n}\n")


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
					mimes = {}
					for format_name in formats:
						mime = Mime("", 0, 0, [], 0, 0)
						for var in strs:
							val = dicts[var][format_name]
							short_var = var.replace("mime_", "").replace("mimes_", "").replace("files_", "").replace("_type", "")
							if short_var in ignores:
								continue
							setattr(mime, short_var, val)
						mimes[mime.ext] = mime
						write_mimes_dict(out_fp, mimes)

			except ModuleNotFoundError:
				logging.exception(f"Could not load {module_name}")

		hashes_dir = os.path.join(root_dir, "hashes")
		for file in os.listdir(hashes_dir):
			hashes = {}
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
							hashes[int(k)] = v
				write_hashes_dict(os.path.join(out_dir, "hashes.py"), hashes)


if __name__ == '__main__':
	ConstantsConverter()
