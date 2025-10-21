import logging
import math
import os
import time
import re
import shutil

import bpy
import mathutils

from generated.formats.ms2.structs.LodInfo import LodInfo
from generated.formats.ms2.structs.Object import Object
from generated.formats.ms2.structs.Model import Model
from generated.formats.ms2.structs.ModelInfo import ModelInfo
from generated.formats.ms2.structs.BoneInfo import BoneInfo
from generated.formats.ms2 import Ms2File, set_game
from plugin.modules_export.armature import export_bones_custom, get_armatures_collections
from plugin.modules_export.collision import export_bounds
from plugin.modules_export.geometry import export_model, scale_bbox
from plugin.modules_export.material import export_material
from plugin.modules_import.armature import get_bone_names
from plugin.utils.object import ensure_visible, has_data_in_coll, get_property
from plugin.utils.lods import get_lod_collections


def get_next_backup_filename(filepath):
	""" Based on the input file name, find copies of the file including ~number """
	sfolder, sfile = os.path.split(os.path.normpath(filepath))
	sname, sext = os.path.splitext(sfile)
	prefixed = [filename for filename in os.listdir(sfolder) if filename.startswith(sname)]
	if len(prefixed) == 0:
		# no files found, create the first one 
		return os.path.join(sfolder, sname + '~1' + sext)
	else:
		# files found, find all the file suffix numbers
		file_suffixes = [0, ]

		for file in prefixed:
			regex_match = re.match(sname + "~(\d+)", file)
			if regex_match:
				file_suffix = regex_match.groups()[0]
				file_suffix_int = int(file_suffix)
				file_suffixes.append(file_suffix_int)

		# get max and increment by one				
		new_suffix = max(file_suffixes) + 1
		return os.path.join(sfolder, sname + '~' + str(new_suffix) + sext)


def save(reporter, filepath='', backup_original=True, apply_transforms=False, update_rig=False, use_stock_normals_tangents=False):
	start_time = time.time()

	ms2 = Ms2File()
	from_scratch = not os.path.isfile(filepath)
	if from_scratch:
		logging.warning(f"{filepath} does not exist. Trying to build ms2 from scratch.")
		update_rig = True
	else:
		ms2.load(filepath)
		ms2.clear()
		if backup_original:
			logging.info(f"Saving a copy of {filepath} in the Backups/ subfolder...")
			old_dir, name = os.path.split(os.path.normpath(filepath))
			exp_dir = os.path.join(old_dir, "backups")
			os.makedirs(exp_dir, exist_ok=True)

			export_path = os.path.join(exp_dir, name)

			backup_name = get_next_backup_filename(export_path)
			shutil.copy(filepath, backup_name)

	logging.info(f"Exporting {filepath}...")

	ms2.read_editable = True
	found_mdl2s = 0

	model_info_lut = {model_info.name: model_info for model_info in ms2.model_infos}
	# clear out any existing model_infos
	ms2.model_infos.clear()
	scene = bpy.context.scene
	game = scene.cobra.game
	set_game(ms2.context, game)
	set_game(ms2.info, game)
	if ms2.context.version < 32:
		raise AttributeError(f"Export not supported for '{game}'")

	armatures_collections = get_armatures_collections(scene)
	last_armature = None

	with ensure_visible():
		for b_armature_ob, mdl2_coll in armatures_collections:
			if from_scratch:
				model_info = ModelInfo(ms2.context)
				model_info.name = mdl2_coll.name
				# create a new armature, might replace it with a previous one later
				model_info.bone_info = BoneInfo(ms2.context)
				model_info.model = Model(ms2.context, model_info)
			else:
				if mdl2_coll.name not in model_info_lut:
					reporter.show_warning(f"MDL2 '{mdl2_coll.name}' was not found in MS2, skipping")
					continue
				model_info = model_info_lut[mdl2_coll.name]
			logging.info(f"Exporting {mdl2_coll.name}")
			# shared armature export?
			if last_armature and b_armature_ob == last_armature and ms2.model_infos:
				logging.info(f"Sharing previous armature")
				# there is a previous armature and we use the same again, so dupe it
				model_info.bone_info = ms2.model_infos[-1].bone_info
			# store model_info
			ms2.model_infos.append(model_info)
			last_armature = b_armature_ob
			found_mdl2s += 1

			model_info.render_flag._value = get_property(mdl2_coll, "render_flag", 0)
			# ensure that we have objects in the scene
			if not has_data_in_coll(mdl2_coll):
				raise AttributeError(f"No objects in collection '{mdl2_coll.name}', nothing to export!")

			if not b_armature_ob:
				reporter.show_warning(f"No armature was found in collection '{mdl2_coll.name}' - did you delete it?")
			else:
				# clear pose
				for pbone in b_armature_ob.pose.bones:
					pbone.matrix_basis = mathutils.Matrix()
				if update_rig:
					export_bones_custom(b_armature_ob, model_info)

			# used to get index from bone name for faster weights
			bones_table = dict(((b, i) for i, b in enumerate(get_bone_names(model_info))))

			b_models = []
			b_materials = []
			lod_collections = get_lod_collections(mdl2_coll)
			if lod_collections and lod_collections[0].objects:
				export_bounds([scale_bbox(ob, apply_transforms) for ob in lod_collections[0].objects], model_info)
			model_info.pack_base = ms2.get_pack_base(model_info.bounds_min, model_info.bounds_max)
			model_info.precision = ms2.get_precision(model_info.pack_base)
			# logging.info(f"chose pack_base = {model_info.pack_base}")
			stream_index = 0
			for lod_i, lod_coll in enumerate(lod_collections):
				m_lod = LodInfo(ms2.context)
				m_lod.distance = get_property(lod_coll, "distance", default=math.pow(30 + 15 * lod_i, 2))
				m_lod.first_object_index = len(model_info.model.objects)
				m_lod.objects = []
				m_lod.stream_index = stream_index
				model_info.model.lods.append(m_lod)
				mesh_in_lod = 0
				for b_ob in lod_coll.objects:
					logging.debug(f"Exporting b_ob {b_ob.name}")
					b_me = b_ob.data
					# JWE2 fur sets this as a mesh property
					shell_count = get_property(b_me, "shell_count", default=0)
					if shell_count > 0:
						indices = range(shell_count)
					else:
						indices = (0,)
					for shell_index in indices:
						logging.debug(f"Exporting shell index {shell_index}")
						if b_me not in b_models:
							b_models.append((b_me, shell_index))
							wrapper = export_model(
								model_info, lod_coll, b_ob, b_me, bones_table, apply_transforms,
								use_stock_normals_tangents, m_lod, shell_index, shell_count, mesh_in_lod)
							wrapper.mesh.lod_index = lod_i
							wrapper.mesh.stream_info.pool_index = stream_index
							mesh_in_lod += 1
						for b_mat in b_me.materials:
							logging.debug(f"Exporting material {b_mat.name}")
							if b_mat not in b_materials:
								b_materials.append(b_mat)
								export_material(model_info, b_mat, reporter)
								if len(b_materials) > 16:
									raise IndexError(
										f"Material {b_mat.name} exceeds the limit of 16 unique materials\n"
										f"and will render with a different material ingame (wraps around)")
							# create one unique mesh per material
							m_ob = Object(ms2.context)
							m_ob.mesh_index = b_models.index((b_me, shell_index))
							m_ob.material_index = b_materials.index(b_mat)

							model_info.model.objects.append(m_ob)
							mesh = model_info.model.meshes[m_ob.mesh_index].mesh
							m_ob.mesh = mesh
							if mesh.context.version >= 52:
								logging.debug(f"Setting chunk material indices")
								for tri_chunk in mesh.tri_chunks:
									tri_chunk.material_index = m_ob.material_index
							m_lod.objects.append(m_ob)
				m_lod.last_object_index = len(model_info.model.objects)
				if lod_i < scene.cobra.num_streams:
					stream_index += 1
	# write ms2, backup should have been created earlier
	ms2.save(filepath)
	# print(ms2)
	if found_mdl2s:
		reporter.show_info(f"Exported {scene.name} in {time.time() - start_time:.2f} sec")
	else:
		mdl2_names = sorted(model_info_lut.keys())
		mdl2_names_str = '\n'.join(mdl2_names)
		reporter.show_warning(
			f"Found no collections matching MDL2s in MS2:\n"
			f"{mdl2_names_str}\n"
			f"Rename your collections to match the MDL2s")

