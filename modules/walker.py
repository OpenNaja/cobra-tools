import io
import os
import logging
import subprocess
from collections import Counter
from pathlib import Path

from modules.formats.FGM import FgmContext
from modules.formats.shared import walk_type, fnv1_32
from ovl_util.logs import ANSI
from constants.converter import write_mimes_dict, write_hashes_dict, write_audio_dict
from generated.array import Array
from generated.formats.fgm.compounds.FgmHeader import FgmHeader
from generated.formats.manis.compounds.ManiInfo import ManiInfo
from generated.formats.ms2.enums.CollisionType import CollisionType

from generated.formats.ms2 import Ms2File, is_pc
from generated.formats.ovl import OvlFile
from generated.formats.ovl_base.versions import games
from constants import Mime, Shader, ConstantsProvider

# get this huge dict from fgm walker, use in ms2 walker
shader_map = {}
# No longer using only content* due to Warhammer Ages of Sigmar adding random folder names
valid_packages = (
"GameMain", "Content", "Campaign", "DLC", "Ghur", "Kruleboyz", "Nighthaunt", "NoFaction", "Stormcast", "Tzeentch")


def content_folder(filepath: Path):
	"""Return the Content folder in filepath"""
	if filepath.parent.name in ("ovldata", "walker_export"):
		return filepath
	for p in filepath.parents:
		if p.parent.name in ("ovldata", "walker_export"):
			return p
	return None


def filter_accept_official(filepath):
	"""Filters filepaths to only accept official content, discards any user-made content"""
	filepath = Path(filepath)
	content_path = content_folder(filepath)
	if not content_path:
		return False

	if any(p in content_path.name for p in valid_packages):
		return True
	# logging.warning(f"Ignoring user-made {filepath.relative_to(content_path.parent)}")
	return False


def filter_accept_all(filepath):
	return True


def search_for_files_in_ovls(gui, start_dir, search_str):
	if start_dir:
		with gui.reporter.log_duration(f"Searching"):
			res = []
			with gui.log_level_override("WARNING"):
				ovl_files = walk_type(start_dir, extension=".ovl")
				ovl_data = OvlFile()
				for ovl_path in gui.reporter.iter_progress(ovl_files, "Searching"):
					try:
						file_names = ovl_data.load(ovl_path, commands={"generate_names": True, "game": gui.ovl_game_choice.entry.currentText()})
						res.extend([
							# remove the leading slash for ovl path, else it is interpreted as relative to C:
							[file_name, os.path.splitext(file_name)[1], os.path.relpath(ovl_path, start_dir)]
							for file_name in file_names if search_str in file_name
						])
					except:
						logging.warning(f"Couldn't read {ovl_path}")
				gui.search_files.emit([search_str, res])


def generate_hash_table(gui, start_dir):
	hashes = {}
	if start_dir:
		with gui.reporter.log_duration(f"Reading hashes"):
			# don't use internal data
			ovl_data = OvlFile()
			all_deps_exts = set()
			# these are the input for which hashes should be stored
			hash_exts = {'.enumnamer', '.lua', '.model2stream', '.particleatlas', '.prefab', '.specdef', '.tex'}
			# when specdef and prefab are left out of the hash table, jwe2 hashtable shrinks from 25 MB down to 0.8MB
			# but that would need to make sure the respective files don't raise warnings on opening
			# hash_exts = {'.enumnamer', '.lua', '.model2stream', '.particleatlas', '.tex'}
			# plain arrays without fields, np vectorized arrays with tuple of field names
			lists = {"mimes_name": (), "mimes_triplets": (), "mimes": ("mime_hash", "mime_version"), "files": ("pool_type", "set_pool_type")}

			mimes = {}
			error_files = []
			ovl_files = walk_type(start_dir, extension=".ovl")
			for ovl_path in gui.reporter.iter_progress(ovl_files, "Hashing"):
				if not filter_accept_official(ovl_path):
					continue
				try:
					# read ovl file
					new_hashes, new_exts = ovl_data.load(ovl_path, commands={"generate_hash_table": hash_exts, "game": gui.ovl_game_choice.entry.currentText()})
					all_deps_exts.update(new_exts)
					for list_id, attribs in lists.items():
						array = getattr(ovl_data, list_id)
						if attribs:
							arrays = {att: array[att] for att in attribs if att in array.dtype.fields}
						else:
							arrays = {list_id: array}
						exts = [f".{ext}" for ext in ovl_data.mimes_ext] if "mimes" in list_id else ovl_data.files_ext
						for list_name, subarray in arrays.items():
							for ext, v in zip(exts, subarray):

								short_var = list_name.replace("mime_", "").replace("mimes_", "").replace("files_", "").replace("_type", "")
								if short_var == "triplets":
									v = [(t.a, t.b, t.c) for t in v]
								# if the value already exists, make sure it is indeed constant (for this version)
								if ext in mimes:
									v_old = getattr(mimes[ext], short_var)
									if v != v_old and v_old:
										logging.warning(f"{list_name}.{short_var} is not constant for {ext}! ({v} vs. {v_old})")
								else:
									mimes[ext] = Mime("", 0, 0, [], 0, 0)
								setattr(mimes[ext], short_var, v)
					hashes.update(new_hashes)
				except:
					logging.exception(f"Reading {ovl_path} failed")
					error_files.append(ovl_path)
			if error_files:
				logging.error(f"{error_files} caused errors!")
			out_dir = get_game_constants_dir(start_dir)
			os.makedirs(out_dir, exist_ok=True)
			# with open(os.path.join(out_dir, "hashes.json"), "w") as json_writer:
			# 	json.dump(hashes, json_writer, indent="\t", sort_keys=True)
			write_hashes_dict(os.path.join(out_dir, "hashes.py"), hashes)
			write_mimes_dict(os.path.join(out_dir, "mimes.py"), mimes)
		logging.info(f"Formats used in dependencies: {[s.replace(':', '.') for s in sorted(all_deps_exts)]}")


def get_game_constants_dir(start_dir):
	# Find a matching game
	constants_dir = Path(__file__).resolve().parent.parent / "constants"
	for game in reversed(games):
		if game.value in start_dir:
			return constants_dir / game.value

	# Game not found
	if "ovldata" in start_dir:
		ovldata_path = start_dir[:start_dir.index("ovldata") + len("ovldata")]
		game_name = Path(ovldata_path).parent.name
		constants_dir = constants_dir / game_name
		logging.warning(f"Could not find a game matching {game_name}")

	if not constants_dir.exists():
		logging.info(f"Creating folder in {constants_dir}")
		constants_dir.mkdir()
	return constants_dir


def bulk_test_models(gui, start_dir, walk_ovls=True, official_only=True, walk_models=True):
	errors = []
	if start_dir:
		export_dir = os.path.join(start_dir, "walker_export")

		ms2_data = Ms2File()
		if walk_ovls:
			bulk_extract_ovls(errors, export_dir, gui, start_dir, (".ms2", ".model2stream"))

		# holds different types of flag - list of byte maps pairs
		type_dic = {}
		blend_modes = set()
		shaders = {}
		materials = set()
		# for last_count
		last_counts = set()
		pack_bases = set()
		constraints_0 = set()
		constraints_1 = set()
		no_bones = set()
		mesh_w = set()
		mesh_collision = set()
		max_bones = -1
		max_bones_ms2 = None
		joint_names_padding = {}
		joint_names_total = {}
		rigid_body_flags = set()
		joint_names_2 = {}
		hc_starts = {}
		pack_bases = set()
		chunk_mesh_zero = set()
		classification_name = set()
		surface_name = set()
		surface_name2 = set()
		zeros_count = set()
		joint_pad_size = {}
		if walk_models:
			with gui.reporter.log_duration("Walking MS2 files"):
				ms2_files = walk_type(export_dir, extension=".ms2")
				for ms2_path in gui.reporter.iter_progress(ms2_files, "Walking MS2 files"):
					if official_only and not filter_accept_official(ms2_path):
						continue
					ms2_path_rel = ms2_path.replace(export_dir, "")
					ms2_name = os.path.basename(ms2_path)
					try:
						# script = f"import bpy;bpy.ops.import_scene.cobra_ms2(filepath='{ms2_path}')"
						# call = f'blender -b --python-expr "{script}"'
						# res = subprocess.check_call(call)
						# print(res)
						ms2_data.load(ms2_path, read_editable=True)
						for mdl2_name, model_info in zip(ms2_data.mdl_2_names, ms2_data.model_infos):
							for i, mat in enumerate(model_info.model.materials):
								blend_modes.add(mat.blend_mode)
								if mat.name not in materials:
									materials.add(mat.name)
								fgm = mat.name.lower()
								if shader_map:
									shader = shader_map[fgm]
									if mat.blend_mode not in shaders:
										shaders[mat.blend_mode] = set()
									shaders[mat.blend_mode].add(shader.lower())
							for i, wrapper in enumerate(model_info.model.meshes):
								mesh_id = f"{mdl2_name}[{i}] in {ms2_name}"
								mesh = wrapper.mesh
								if hasattr(mesh, "vert_chunks"):
									chunk_mesh_zero.add(mesh.zero)
									for v in mesh.vert_chunks:
										pack_bases.add((v.pack_base, v.precision))
								flag = int(mesh.flag)
								if flag not in type_dic:
									type_dic[flag] = ([], [])
								type_dic[flag][0].append(mesh_id)
								if hasattr(mesh, "uv_offset_2"):
									mesh_w.add((bool(mesh.uv_offset_2), int(mesh.flag)))
							# 	type_dic[model.flag][1].append((model.bytes_mean, model.bytes_max, model.bytes_min))
							last_counts.add(model_info.last_count)
							# pack_bases.add(model_info.pack_base)
							pack_bases.add((model_info.pack_base, model_info.precision))
							if model_info.bone_info:
								zeros_count.add(model_info.bone_info.zeros_count)
								if model_info.bone_info.bone_count > max_bones:
									max_bones = model_info.bone_info.bone_count
									max_bones_ms2 = ms2_path_rel
								if model_info.bone_info.joint_count:
									joints = model_info.bone_info.joints
									s = joints.start_pc.io_size
									if s not in joint_pad_size:
										joint_pad_size[s] = set()
									joint_pad_size[s].add(model_info.bone_info.bone_count)
									joint_names_padding[(joints.joint_names.io_size, joints.joint_names_padding.io_size+joints.after_names.io_size, )] = ms2_path_rel
									hcs = sum(len(j.hitchecks) for j in joints.joint_infos)
									joint_names_2[(joints.after_names.io_size, hcs, )] = ms2_path_rel
									# print(joints)
									# joint_names_total[joints.joint_names.io_size+joints.joint_names_padding.io_size] = ms2_path_rel
									# joint_names_2[joints.joint_names.io_start - joints.names_ref_pc.io_start + joints.joint_names.io_size+joints.joint_names_padding.io_size] = ms2_path_rel
									# if model_info.bone_info.joints.count_0:
									# 	constraints_0.add(ms2_path)
									# if model_info.bone_info.joints.count_1:
									# 	constraints_1.add(ms2_path)
									for rb in joints.rigid_body_list:
										rigid_body_flags.add(int(rb.flag))
									for j in joints.joint_infos:
										# PC - discard invalid flags
										if j.context.version == 32 and j.eleven != 11:
											continue
										for hit in j.hitchecks:
											hc_starts[hit.io_start-ms2_data.models_reader.io_start] = ms2_path_rel
											classification_name.add(hit.classification_name)
											surface_name.add(hit.surface_name)
											if is_pc(hit.context):
												# surface_name2.add((hit.surface_name, int(hit.surface_name_2)))
												surface_name2.add((hit.surface_name, hit.surface_name_2))
											if hit.dtype == CollisionType.MESH_COLLISION:
												mesh_collision.add(ms2_path_rel)
							else:
								no_bones.add(ms2_path_rel)
					except Exception as ex:
						logging.exception("Walking models errored")
						errors.append((ms2_path, ex))
			# report
			print(f"\nThe following {len(errors)} errors occured:")
			for file_path, ex in errors:
				print(file_path, str(ex))

			print("\nThe following type - map pairs were found:")
			print(sorted(type_dic.keys()))
			for flag, tup in sorted(type_dic.items()):
				print(flag)
				names, maps_list = tup
				print("Some files:", list(sorted(set(names)))[:25])
				print("num meshes", len(names))
			print(f"last_counts: {last_counts}")
			print(f"chunk_mesh_zero: {chunk_mesh_zero}")
			print(f"constraints_0: {constraints_0}")
			print(f"constraints_1: {constraints_1}")
			print(f"no_bones: {no_bones}")
			print(f"mesh_collision: {mesh_collision}")
			print(f"Max bones: {max_bones} in {max_bones_ms2}")
			print(f"pack_bases: {pack_bases}")
			print(f"joint_pad_size: {joint_pad_size}")
			# print(f"blend_modes: {blend_modes}")
			if shader_map:
				print(f"shaders: {shaders}")
			print(f"rigid_body_flags: {rigid_body_flags}")
			print(f"classification_name: {sorted(classification_name)}")
			print(f"surface_name: {sorted(surface_name)}")
			print(f"surface_name2: {sorted(surface_name2)}")
			print(f"mesh_w: {mesh_w}")
			print(f"materials: {sorted(materials)}")
			print(f"zeros_count: {sorted(zeros_count)}")
			# largest_zstring_buffers = sorted(joint_names_padding.keys())
			# num = 10
			# if len(largest_zstring_buffers) > num:
			# 	for k in largest_zstring_buffers[-num:]:
			# 		logging.info(f"Found {k} for {joint_names_padding[k]}")
			# logging.info(largest_zstring_buffers)
			# logging.info(Counter(joint_names_padding.keys()))
			# logging.info(Counter(joint_names_total.keys()))
			# totals = sorted(k for k in joint_names_total.keys())
			# for t in totals:
			# 	logging.info(f"{t} mod = {t % 32}")
			# totals = sorted(k for k in joint_names_2.keys())
			# for t in totals:
			# 	logging.info(f"{t} mod = {t % 32}")
			# totals = sorted(k for k in hc_starts.keys())
			# for t in totals:
			# 	logging.info(f"{t} mod = {t % 16}, {t % 64}")
			# for (size, count), fp in joint_names_2.items():
			# 	logging.info(f"size {size} / count {count} = {size/count} in {fp}")


def ovls_in_path(gui, start_dir, only_types):
	ovl_data = OvlFile()
	ovl_data.load_hash_table()
	ovl_files = walk_type(start_dir, extension=".ovl")
	for ovl_path in gui.reporter.iter_progress(ovl_files, "Walking OVL files"):
		try:
			# read ovl file
			ovl_data.load(ovl_path, commands={"only_types": only_types, "game": gui.ovl_game_choice.entry.currentText()})
			yield ovl_data, ovl_path
		except Exception as ex:
			logging.exception(f"Opening OVL failed: {ovl_path}")
			# errors.append((ovl_path, ex))


def bulk_extract_ovls(errors, export_dir, gui, start_dir, only_types):
	for ovl_data, ovl_path in ovls_in_path(gui, start_dir, only_types):
		try:
			# create an output folder for it
			rel_p = os.path.relpath(ovl_path, start=start_dir)
			rel_d = os.path.splitext(rel_p)[0]
			out_dir = os.path.join(export_dir, rel_d)
			ovl_data.extract(out_dir, only_types=only_types)
		except Exception as ex:
			logging.exception(f"Extracting OVL failed: {ovl_path}")
			errors.append((ovl_path, ex))


def write_shader(file, textures, attributes):
	file.write("\t\t[\n")
	for tex_name in sorted(textures):
		file.write(f"\t\t\t'{tex_name}',\n")
	file.write("\t\t],\n")
	file.write("\t\t{\n")
	for attr_name, attr in sorted(attributes):
		file.write(f"\t\t\t'{attr_name}': {attr},\n")
	file.write("\t\t}\n")
	file.write("\t),\n")


def write_shaders(file, shaders):
	file.write("shaders = {\n")
	for shader_name, shader in sorted(shaders.items()):
		file.write(f"\t'{shader_name}': (\n")
		write_shader(file, shader.textures, shader.attributes.items())
	file.write("}\n")


def write_shaders_dict(file, shaders):
	file.write("shaders = {\n")
	for shader_name, shader in sorted(shaders.items()):
		file.write(f"\t'{shader_name}': (\n")
		write_shader(file, shader[0], shader[1].items())
	file.write("}\n")


def get_fgm_values(gui, game_dir, walk_dir="", walk_ovls=True, official_only=True, full_report=False):
	errors = []
	warnings = []
	# Detect if walk_dir is a game directory or subfolder
	in_installed_game = Path(game_dir) in Path(walk_dir).parents or game_dir == walk_dir
	base_dir = game_dir if in_installed_game else walk_dir
	walk_dir = base_dir if not walk_dir else walk_dir
	if base_dir and walk_dir:
		# Set and make export directory
		export_dir = os.path.join(base_dir, "walker_export")
		Path(export_dir).mkdir(exist_ok=True)
		# Full ovldata walk or subfolder
		full_game_walk = in_installed_game and walk_dir == base_dir
		if walk_ovls:
			bulk_extract_ovls(errors, export_dir, gui, walk_dir, (".fgm",))
		shaders = {}
		shaders_added = {}
		shaders_removed = {}
		new_shader_fgms = {}
		# used to debug the mapping of blend modes in ms2 material slots to predict them
		fgm_to_shader = {}

		# The game assigned to the FGMs (assumes all walked FGMs are from the same game)
		fgm_game = "Unknown Game"
		# Create sets of all shader names per game
		game_shaders = {"Unknown Game": []}
		constants = ConstantsProvider()
		for game in constants:
			game_shaders[game] = set(constants[game].get("shaders", {}).keys())
		# To remove shaders as they are discovered
		undiscovered_shaders = game_shaders.copy()

		context = FgmContext()
		fgm_files = walk_type(walk_dir, extension=".fgm")
		for fgm_path in gui.reporter.iter_progress(fgm_files, "Walking FGM files"):
			if official_only and not filter_accept_official(fgm_path):
				continue
			try:
				header = FgmHeader.from_xml_file(fgm_path, context)
				shader_name = header.shader_name
				if shader_name not in shaders:
					# shaders[shader_name] = ([], {})
					shaders[shader_name] = Shader(set(), {})
				shader = shaders[shader_name]

				# Resolve shaders.py for the FGM's game, and check for presence
				game_enum = header.game.replace("Games.", "")
				if game_enum in games.__members__:
					game = games[game_enum].value
					# Set the game to access the correct constants
					fgm_game = game
					if game in constants.keys() and "shaders" in constants[game]:
						logging.debug(f"Checking presence of {shader_name} for constants\\{game}")
						if shader_name not in constants[game]["shaders"]:
							# New shader found in FGM
							shaders_added[shader_name] = shader
							if shader_name in new_shader_fgms.keys():
								new_shader_fgms[shader_name].add(fgm_path)
							else:
								new_shader_fgms[shader_name] = set([fgm_path])
						else:
							# Existing shader
							logging.debug(f"{shader_name} found in constants\\{game}")
							undiscovered_shaders[game].discard(shader_name)

				# for ms2 debugging
				# fgm_name = os.path.basename(fgm_path)
				# fgm_to_shader[os.path.splitext(fgm_name)[0].lower()] = shader_name
				for attrib, attrib_data in zip(header.attributes.data, header.value_foreach_attributes.data):
					val = tuple(attrib_data.value)
					if attrib.name not in shader.attributes:
						shader.attributes[attrib.name] = (int(attrib.dtype), [])
					shader.attributes[attrib.name][1].append(val)
				for texture in header.textures.data:
					shader.textures.add(texture.name)

			except Exception as ex:
				logging.exception(f"FGM Inspection Error: {fgm_path}")
				errors.append((fgm_path, ex))

		for shader_name, shader in shaders.items():
			# only keep the five most common for this shader
			for att, val in shader.attributes.items():
				shader.attributes[att] = (val[0], Counter(v for v in val[1]).most_common(5))

		# Write to tools dir constants if full ovldata inspection, otherwise walker_export
		out_dir = get_game_constants_dir(base_dir) if full_game_walk else export_dir
		with open(os.path.join(out_dir, "shaders.py"), "w+") as f:
			write_shaders(f, shaders)
		logging.success(f"shaders.py written to {Path(out_dir)}")

		# Dump new shaders
		if shaders_added:
			with open(os.path.join(export_dir, "shaders_added.py"), "w+") as f:
				write_shaders(f, shaders_added)
			logging.success(f"shaders_added.py written to {Path(export_dir)}")

		# Output errors
		if errors:
			error_string = f"The following errors occurred:{ANSI.LIGHT_YELLOW}\n "
			for file_path, ex in errors:
				error_string += f"{file_path}\n {str(ex)}"
			logging.error(error_string)

		# Hide excess output
		if not full_report:
			return

		# Dump potential deprecations
		if shaders_removed:
			with open(os.path.join(export_dir, "shaders_removed.py"), "w+") as f:
				write_shaders_dict(f, shaders_removed)
			logging.success(f"shaders_removed.py written to {Path(export_dir)}")

		# Generate warnings
		for shader_name, fgms in new_shader_fgms.items():
			fgm_list = ""
			for fgm in fgms:
				fgm_list += f"    {fgm.replace(walk_dir, '')[1:]}\n"
			msg_new_used_by = f"{shader_name} missing from constants\\{fgm_game}, used by:\n{fgm_list}"
			warnings.append((msg_new_used_by, ""))

		for shader_name in undiscovered_shaders[fgm_game]:
			shaders_removed[shader_name] = constants[fgm_game]["shaders"][shader_name]
			msg_not_found = f"{shader_name} in constants\\{fgm_game} was not found during walking."
			warnings.append((msg_not_found, ""))

		# Output warnings
		if warnings:
			warning_string = f"The following warnings occurred:{ANSI.LIGHT_YELLOW}\n "
			for file_path, ex in warnings:
				warning_string += f"{file_path}\n {str(ex)}"
			logging.warning(warning_string)


def add_key(dic, k, v):
	if k not in dic:
		dic[k] = set()
	dic[k].add(v)


def get_manis_values(gui, start_dir, walk_ovls=True, official_only=True):
	errors = []
	data = {}
	dtype_to_files = {}
	scale_0_to_files = {}
	dtype_0_to_files = {}
	dtype_to_counts = {}
	dtype_quant_to_counts = {}
	unk_counts = {}
	if start_dir:
		for ovl_data, ovl_path in ovls_in_path(gui, start_dir, (".manis", ".mani",)):
			if official_only and not filter_accept_official(ovl_path):
				continue
			ovl_name = os.path.basename(ovl_path)
			ovl_name = os.path.splitext(ovl_name)[0]
			try:
				for loader in ovl_data.loaders.values():
					# print(loader.name)
					if loader.ext == ".manis":
						stream = io.BytesIO(loader.data_entry.buffers[0].data + b"\x00\x00")
						mani_infos = Array.from_stream(stream, loader.context, 0, None, (len(loader.children), ), ManiInfo)

						for mani_info in mani_infos:
							dtype = int(mani_info.dtype)
							# print(mani_info)
							# if mani_info.dtype.compression != 0:
							# 	dtype_quant_to_counts
							# add_key(unk_counts, (mani_info.root_pos_bone, mani_info.root_ori_bone), f"{ovl_name}.{loader.basename}")
							add_key(dtype_to_files, dtype, ovl_name)
							add_key(dtype_to_counts, dtype, (
								bool(mani_info.pos_bone_count),
								bool(mani_info.ori_bone_count),
								bool(mani_info.scl_bone_count),
								bool(mani_info.float_count))
									)
							if mani_info.dtype.compression == 0 and (mani_info.pos_bone_count or mani_info.ori_bone_count or mani_info.scl_bone_count):
								add_key(dtype_0_to_files, dtype, f"{ovl_name}.{loader.basename}")
								if mani_info.scl_bone_count:
									add_key(scale_0_to_files, dtype, ovl_name)
			except:
				logging.exception(f"Failed")
	# for k, strings in sorted(data.items()):
	# 	logging.info(f"{k} - {len(strings)} - {k/len(strings)}- {sum(len(s) for s in strings)}")

	try:
		logging.info(f"dtype - files map")
		for dtype, files in sorted(dtype_to_files.items()):
			logging.info(f"dtype {dtype} - files {sorted(files)[:10]}")
		logging.info(f"dtype uncompressed - files map")
		for dtype, files in sorted(dtype_0_to_files.items()):
			logging.info(f"dtype {dtype} - files {sorted(files)}")
		logging.info(f"scale on uncompressed - files map")
		for dtype, files in sorted(scale_0_to_files.items()):
			logging.info(f"dtype {dtype} - files {sorted(files)}")
		logging.info(f"dtype_to_counts map")
		for dtype, files in sorted(dtype_to_counts.items()):
			logging.info(f"dtype {dtype} - files {sorted(files)}")
		# logging.info(f"unk_counts map")
		# for dtype, files in sorted(unk_counts.items()):
		# 	logging.info(f"unk count {dtype} - {len(files)} files {sorted(files)[:10]}")
	except:
		logging.exception(f"Failed")


def get_audio_names(gui, start_dir, walk_ovls=True, official_only=True):
	names = {}
	if start_dir:
		for ovl_data, ovl_path in ovls_in_path(gui, start_dir, (".motiongraph",)):
			if official_only and not filter_accept_official(ovl_path):
				continue
			ovl_name = os.path.basename(ovl_path)
			ovl_name = os.path.splitext(ovl_name)[0]
			try:
				for loader in ovl_data.loaders.values():
					# print(loader.name)
					if loader.ext == ".motiongraph":
						for s in loader.get_audio_strings():
							h = fnv1_32(s.lower().encode())
							names[h] = s
							# print(s)
			except:
				logging.exception(f"Failed")

		out_dir = get_game_constants_dir(start_dir)
		os.makedirs(out_dir, exist_ok=True)
		write_audio_dict(os.path.join(out_dir, "audio.py"), names)

