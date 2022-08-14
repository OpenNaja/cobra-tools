import os
import time
import traceback
import logging
import numpy as np
from collections import defaultdict, Counter

from generated.formats.fgm.compounds.FgmHeader import FgmHeader
from generated.formats.ovl_base import OvlContext

from generated.formats.ms2 import Ms2File
from generated.formats.ovl import OvlFile
from ovl_util import interaction
from root_path import root_dir


def walk_type(start_dir, extension=".ovl"):
	logging.info(f"Scanning {start_dir} for {extension} files")
	ret = []
	for root, dirs, files in os.walk(start_dir, topdown=False):
		for name in files:
			if name.lower().endswith(extension):
				ret.append(os.path.join(root, name))
	return ret


def generate_hash_table(gui, start_dir):
	hash_dict = {}
	if start_dir:
		# don't use internal data
		ovl_data = OvlFile()
		dic = {}
		lists = {"mimes": ("name", "mime_hash", "mime_version", "triplet_count", "triplets"), "files": ("pool_type", "set_pool_type")}
		for list_name, attr_names in lists.items():
			dic[list_name] = {}
			for attr_name in attr_names:
				dic[list_name][attr_name] = {}
		error_files = []
		ovl_files = walk_type(start_dir, extension=".ovl")
		of_max = len(ovl_files)
		for of_index, ovl_path in enumerate(ovl_files):
			gui.update_progress("Hashing names: " + os.path.basename(ovl_path), value=of_index, vmax=of_max)
			try:
				# read ovl file
				new_hashes = ovl_data.load(ovl_path, commands={"generate_hash_table": True})
				for list_name, attr_names in lists.items():
					for entry in getattr(ovl_data, list_name):
						for attr_name in attr_names:
							v = getattr(entry, attr_name)
							if attr_name == "triplets":
								v = [(t.a, t.b, t.c) for t in v]
							# if the value already exists, make sure it is indeed constant (for this version)
							if entry.ext in dic[list_name][attr_name]:
								if v != dic[list_name][attr_name][entry.ext]:
									logging.error(f"{list_name}.{attr_name} is not constant for {entry.ext}! ({v} vs. {dic[list_name][attr_name][entry.ext]})")
							dic[list_name][attr_name][entry.ext] = v
				hash_dict.update(new_hashes)
			except:
				traceback.print_exc()
				error_files.append(ovl_path)
		# print(dic)
		if error_files:
			logging.error(f"{error_files} caused errors!")
		try:
			# write the hash text file to the hashes folder
			export_dir = os.path.join(root_dir, "hashes")
			out_path = os.path.join(export_dir, f"{os.path.basename(start_dir)}.txt")
			with open(out_path, "w") as f:
				for k, v in hash_dict.items():
					f.write(f"{k} = {v}\n")
			out_path = os.path.join(export_dir, f"constants_{os.path.basename(start_dir)}.py")
			with open(out_path, "w") as f:
				for list_name, attr_names in lists.items():
					for attr_name in attr_names:
						f.write(f"{list_name}_{attr_name} = {dic[list_name][attr_name]}\n\n")

		except BaseException as err:
			print(err)
		logging.info(f"Wrote {len(hash_dict)} items to {out_path}")


def bulk_test_models(gui, start_dir, walk_ovls=True, walk_models=True):
	errors = []
	if start_dir:
		export_dir = os.path.join(start_dir, "walker_export")
		ms2_data = Ms2File()
		if walk_ovls:
			bulk_extract_ovls(errors, export_dir, gui, start_dir, (".ms2",))

		# holds different types of flag - list of byte maps pairs
		type_dic = {}
		# for last_count
		last_counts = set()
		flags = set()
		no_bones = set()
		if walk_models:
			start_time = time.time()
			ms2_files = walk_type(export_dir, extension=".ms2")
			mf_max = len(ms2_files)
			for mf_index, ms2_path in enumerate(ms2_files):
				ms2_name = os.path.basename(ms2_path)
				gui.update_progress(f"Walking MS2 files: {ms2_name}", value=mf_index, vmax=mf_max)
				try:
					# ms2_data.load(ms2_path, map_bytes=True, entry=True)
					ms2_data.load(ms2_path)
					for mdl2_name, model_info in zip(ms2_data.mdl_2_names, ms2_data.model_infos):
						for i, wrapper in enumerate(model_info.model.meshes):
							mesh_id = f"{mdl2_name}[{i}] in {ms2_name}"
							mesh = wrapper.mesh
							if mesh.flag not in type_dic:
								type_dic[mesh.flag] = ([], [])
							type_dic[mesh.flag][0].append(mesh_id)
						# 	type_dic[model.flag][1].append((model.bytes_mean, model.bytes_max, model.bytes_min))
						last_counts.add(model_info.last_count)
						if model_info.bone_info:
							if model_info.bone_info.count_7:
								flags.add(model_info.bone_info.struct_7.flag)
						else:
							no_bones.add(ms2_path)
				except Exception as ex:
					logging.exception("Walking models errored")
					errors.append((ms2_path, ex))
		# report
		print(f"\nThe following {len(errors)} errors occured:")
		for file_path, ex in errors:
			print(file_path, str(ex))

		print("\nThe following type - map pairs were found:")
		for flag, tup in sorted(type_dic.items()):
			print(flag)
			names, maps_list = tup
			print("Some files:", list(sorted(set(names)))[:25])
			print("num meshes", len(names))
			# means, maxs, mins = zip(*maps_list)
			# print(len(means))
			# print("mean", np.mean(means, axis=0).astype(dtype=np.ubyte))
			# print("max", np.max(maxs, axis=0))
			# print("min", np.min(mins, axis=0))
			# print()
		print(f"last_counts: {last_counts}")
		print(f"flags: {flags}")
		print(f"no_bones: {no_bones}")
		msg = f"Loaded {mf_max} models {time.time() - start_time:.2f} seconds"
		logging.info(msg)
		gui.update_progress(msg, value=1, vmax=1)


def bulk_extract_ovls(errors, export_dir, gui, start_dir, only_types):
	# don't use internal data
	ovl_data = OvlFile()
	error_files = []
	ovl_files = walk_type(start_dir, extension=".ovl")
	of_max = len(ovl_files)
	for of_index, ovl_path in enumerate(ovl_files):
		gui.update_progress(f"Walking OVL files: {os.path.basename(ovl_path)}", value=of_index, vmax=of_max)
		try:
			# read ovl file
			ovl_data.load(ovl_path, commands={"only_types": only_types})
			# create an output folder for it
			rel_p = os.path.relpath(ovl_path, start=start_dir)
			rel_d = os.path.splitext(rel_p)[0]
			out_dir = os.path.join(export_dir, rel_d)
			out_paths, error_files_new = ovl_data.extract(out_dir, only_types=only_types)
			error_files += error_files_new
		except Exception as ex:
			traceback.print_exc()
			errors.append((ovl_path, ex))
	interaction.extract_error_warning(error_files)


def get_fgm_values(gui, start_dir, walk_ovls=True, walk_fgms=True):
	errors = []
	if start_dir:
		export_dir = os.path.join(start_dir, "walker_export")
		if walk_ovls:
			bulk_extract_ovls(errors, export_dir, gui, start_dir, (".fgm",))

		attributes = {}
		textures = set()
		shaders = set()
		shader_textures = defaultdict(set)
		shader_attribs = defaultdict(set)
		shader_attrib_stats = defaultdict(Counter)
		if walk_fgms:
			context = OvlContext()
			fgm_files = walk_type(export_dir, extension=".fgm")
			mf_max = len(fgm_files)
			for mf_index, fgm_path in enumerate(fgm_files):
				fgm_name = os.path.basename(fgm_path)
				gui.update_progress(f"Walking FGM files: {fgm_name}", value=mf_index, vmax=mf_max)
				try:
					header = FgmHeader.from_xml_file(fgm_path, context)
					shaders.add(header.shader_name)
					for i, attrib in enumerate(header.attributes.data):
						val = tuple(header.value_foreach_attributes.data[i].value)
						if attributes.get(attrib.name):
							attributes[attrib.name][1].append(val)
						else:
							attributes[attrib.name] = (int(attrib.dtype), [val])
					for texture in header.textures.data:
						textures.add(texture.name)

					shader_textures[header.shader_name] |= {a.name for a in header.textures.data}
					shader_attribs[header.shader_name] |= {a.name for a in header.attributes.data}
					#shader_attrib_stats[header.shader_name].update(frozenset([a.name for a in header.attributes.data]))

				except Exception as ex:
					traceback.print_exc()
					errors.append((fgm_path, ex))

		for att, val in attributes.items():
			attributes[att] = (val[0], Counter(tuple(sorted(tup)) for tup in val[1]).most_common(5))

		# report
		if errors:
			print("\nThe following errors occurred:")
			for file_path, ex in errors:
				print(file_path, str(ex))

		out_path = os.path.join(export_dir, f"fgm_{os.path.basename(start_dir)}.py")
		with open(out_path, "w") as f:
			f.write(f"# Attributes, their dtypes, and {len(list(attributes.values())[0][1])} most common values\n")
			f.write("# To generate full usage values, you must run FGM Walker on all Content FGMs\n")
			f.write("attributes = {\n")
			for att in sorted(attributes.keys()):
				f.write(f'    "{att}": {attributes[att]},\n')
			f.write("}\n\n")
			f.write("textures = {\n")
			for tex in sorted(textures):
				f.write(f'    "{tex}",\n')
			f.write("}\n\n")
			f.write("shaders = {\n")
			for shader in sorted(shaders):
				f.write(f'    "{shader}",\n')
			f.write("}\n\n")
			f.write("shader_textures = {\n")
			for tex in shader_textures.keys():
				f.write(f'    "{tex}":\n         {sorted(shader_textures[tex])},\n\n')
			f.write("}\n\n")
			f.write("shader_attribs = {\n")
			for shader in shader_attribs.keys():
				f.write(f'    "{shader}":\n         {sorted(shader_attribs[shader])},\n\n')
			f.write("}\n\n")
			#f.write("shader_attrib_stats = {\n\n")
			#for shader in shader_attrib_stats.keys():
			#	f.write(f"    '{shader}':\n         {shader_attrib_stats[shader]},\n\n")
			#f.write("}\n\n")
		print(f"Written to {out_path}")
		gui.update_progress("Operation completed!", value=1, vmax=1)
