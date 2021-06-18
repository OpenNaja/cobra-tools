import os
import traceback
import logging
import numpy as np

from generated.formats.ms2 import Mdl2File
from generated.formats.ovl import OvlFile
from ovl_util import interaction


def walk_type(start_dir, extension="ovl"):
	logging.info(f"Scanning {start_dir} for {extension} files")
	ret = []
	for root, dirs, files in os.walk(start_dir, topdown=False):
		for name in files:
			if name.lower().endswith("."+extension):
				ret.append(os.path.join(root, name))
	return ret


def generate_hash_table(gui, start_dir):
	hash_dict = {}
	if start_dir:
		# don't use internal data
		ovl_data = OvlFile()
		error_files = []
		ovl_files = walk_type(start_dir, extension="ovl")
		of_max = len(ovl_files)
		for of_index, ovl_path in enumerate(ovl_files):
			gui.update_progress("Hashing names: " + os.path.basename(ovl_path), value=of_index, vmax=of_max)
			try:
				# read ovl file
				new_hashes = ovl_data.load(ovl_path, commands=("generate_hash_table",))
				hash_dict.update(new_hashes)
			except:
				error_files.append(ovl_path)
		if error_files:
			logging.error(f"{error_files} caused errors!")
		# write the hash text file to the hashes folder
		export_dir = os.path.join(os.getcwd(), "hashes")
		out_path = os.path.join(export_dir, f"{os.path.basename(start_dir)}.txt")
		with open(out_path, "w") as f:
			for k, v in hash_dict.items():
				f.write(f"{k} = {v}\n")
		logging.info(f"Wrote {len(hash_dict)} items to {out_path}")


def bulk_test_models(gui, start_dir, walk_ovls=True, walk_models=True):
	errors = []
	if start_dir:
		export_dir = os.path.join(start_dir, "walker_export")
		# don't use internal data
		ovl_data = OvlFile()
		mdl2_data = Mdl2File()
		if walk_ovls:
			error_files = []
			skip_files = []
			ovl_files = walk_type(start_dir, extension="ovl")
			of_max = len(ovl_files)
			for of_index, ovl_path in enumerate(ovl_files):
				gui.update_progress("Walking OVL files: " + os.path.basename(ovl_path), value=of_index,
									vmax=of_max)
				try:
					# read ovl file
					ovl_data.load(ovl_path, commands=gui.commands)
					# create an output folder for it
					outdir = os.path.join(export_dir, os.path.basename(ovl_path[:-4]))
					out_paths, error_files_new, skip_files_new = ovl_data.extract(outdir, only_types=(".ms2",))
					error_files += error_files_new
					skip_files += skip_files_new
				except Exception as ex:
					traceback.print_exc()
					errors.append((ovl_path, ex))

			interaction.skip_messages(error_files, skip_files)

		# holds different types of flag - list of byte maps pairs
		type_dic = {}
		# for another_count
		another_counts = set()
		if walk_models:
			mdl2_files = walk_type(export_dir, extension="mdl2")
			mf_max = len(mdl2_files)
			for mf_index, mdl2_path in enumerate(mdl2_files):
				mdl2_name = os.path.basename(mdl2_path)
				gui.update_progress("Walking MDL2 files: " + mdl2_name, value=mf_index, vmax=mf_max)
				try:
					mdl2_data.load(mdl2_path, map_bytes=True, entry=True)
					for model in mdl2_data.models:
						if model.flag not in type_dic:
							type_dic[model.flag] = ([], [])
						type_dic[model.flag][0].append(mdl2_name)
						type_dic[model.flag][1].append((model.bytes_mean, model.bytes_max, model.bytes_min))
					another_counts.add(mdl2_data.model_info.another_count)
				except Exception as ex:
					traceback.print_exc()
					errors.append((mdl2_path, ex))
		# report
		print("\nThe following errors occured:")
		for file_path, ex in errors:
			print(file_path, str(ex))

		print("\nThe following type - map pairs were found:")
		for flag, tup in sorted(type_dic.items()):
			print(flag, bin(flag))
			names, maps_list = tup
			print("Some files:", list(set(names))[:25])
			print("num models", len(maps_list))
			means, maxs, mins = zip(*maps_list)
			print(len(means))
			print("mean", np.mean(means, axis=0).astype(dtype=np.ubyte))
			print("max", np.max(maxs, axis=0))
			print("min", np.min(mins, axis=0))
			print()
		print(f"another_counts: {another_counts}")
		gui.update_progress("Operation completed!", value=1, vmax=1)