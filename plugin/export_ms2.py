import logging
import math
import os
import time
import re
import shutil

import bpy
import mathutils
import numpy as np

from generated.formats.ms2.compounds.LodInfo import LodInfo
from generated.formats.ms2.compounds.Object import Object
from generated.formats.ms2.compounds.Model import Model
from generated.formats.ms2.compounds.ModelInfo import ModelInfo
from generated.formats.ms2.compounds.BoneInfo import BoneInfo
from generated.formats.ms2.compounds.packing_utils import PACKEDVEC_MAX
from generated.formats.ms2 import Ms2File, is_jwe2
from plugin.modules_export.armature import get_armature, export_bones_custom
from plugin.modules_export.collision import export_bounds, get_bounds
from plugin.modules_export.geometry import export_model, scale_bbox
from plugin.modules_export.material import export_material
from plugin.modules_import.armature import get_bone_names
from plugin.utils.object import has_objects_in_scene, get_property
from plugin.utils.shell import get_collection_endswith


def get_pack_base(b_obs, apply_transforms=False):
	"""Detect a suitable pack_base value depending on the bounds of b_obs"""
	# todo JWE2 perhaps supports unique pack_base per vert_chunk
	bounds = [scale_bbox(ob, apply_transforms) for ob in b_obs]
	bounds_max, bounds_min = get_bounds(bounds)
	coord_min = np.min(bounds_min)
	coord_max = np.max(bounds_max)
	# use some slight tolerance to avoid wrapping the edge values
	tolerance = 1.05
	for pack_base in [float(2 ** x) for x in range(1, 16)]:
		if -pack_base < coord_min*tolerance and coord_max*tolerance < pack_base:
			return pack_base


def get_next_backup_filename(filepath):
	""" Based on the input file name, find copies of the file including ~number """
	sfolder, sfile = os.path.split(os.path.normpath(filepath))
	sname, sext = os.path.splitext(sfile)
	prefixed = [filename for filename in os.listdir(sfolder) if filename.startswith(sname)]
	if len(prefixed) == 0:
		# no files found, create the first one 
		return os.path.join(sfolder,sname + '~1' + sext)
	else:
		# files found, find all the file suffix numbers
		file_suffixes = []

		for file in prefixed:
			regex_match = re.match(sname + "~(\d+)", file)
			if regex_match:
				file_suffix = regex_match.groups()[0]
				file_suffix_int = int(file_suffix)
				file_suffixes.append(file_suffix_int)

		# get max and increment by one				
		new_suffix = max(file_suffixes) + 1 
		return os.path.join(sfolder,sname + '~' + str(new_suffix) + sext)


def save(filepath='', backup_original=True, apply_transforms=False, update_rig=False, use_stock_normals_tangents=False):
	messages = set()
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
	found_scenes = 0

	model_info_lut = {model_info.name: model_info for model_info in ms2.model_infos}
	for scene in bpy.data.scenes:
		if from_scratch:
			ms2.context.version = ms2.info.version = scene.cobra.version
			model_info = ModelInfo(ms2.context)
			model_info.name = scene.name
			model_info.bone_info = BoneInfo(ms2.context)
			model_info.model = Model(ms2.context, model_info)
			ms2.model_infos.append(model_info)
		else:
			if scene.name not in model_info_lut:
				logging.warning(f"Scene '{scene.name}' was not found in the MS2 file, skipping")
				continue
			model_info = model_info_lut[scene.name]

		found_scenes += 1
		logging.debug(f"Exporting scene {scene.name}")

		# make active scene
		bpy.context.window.scene = scene
		# make all collections visible in view_layer to ensure applying modifiers works
		view_collections = bpy.context.view_layer.layer_collection.children
		view_states = [coll.exclude for coll in view_collections]
		for coll in view_collections:
			coll.exclude = False
		model_info.render_flag._value = get_property(scene, "render_flag")
		# ensure that we have objects in the scene
		if not has_objects_in_scene(scene):
			raise AttributeError(f"No objects in scene '{scene.name}', nothing to export!")

		b_armature_ob = get_armature(scene)
		if not b_armature_ob:
			logging.warning(f"No armature was found in scene '{scene.name}' - did you delete it?")
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
		bounds = []
		lod_collections = []
		for lod_i in range(6):
			lod_coll = get_collection_endswith(scene, f"_LOD{lod_i}")
			if not lod_coll:
				break
			lod_collections.append(lod_coll)
		# set a default even when there are no models
		if lod_collections and lod_collections[0].objects:
			model_info.pack_base = get_pack_base(lod_collections[0].objects, apply_transforms)
		else:
			model_info.pack_base = 512.0
		model_info.precision = model_info.pack_base / PACKEDVEC_MAX
		# logging.debug(f"chose pack_base = {model_info.pack_base} precision = {model_info.precision}")
		stream_index = 0
		for lod_i, lod_coll in enumerate(lod_collections):
			m_lod = LodInfo(ms2.context)
			m_lod.distance = math.pow(30 + 15 * lod_i, 2)
			m_lod.first_object_index = len(model_info.model.objects)
			m_lod.objects = []
			m_lod.stream_index = stream_index
			model_info.model.lods.append(m_lod)
			for b_ob in lod_coll.objects:
				logging.debug(f"Exporting b_ob {b_ob.name}")
				b_me = b_ob.data
				# JWE2 fur sets this as a mesh property
				shell_count = get_property(b_me, "shell_count", default=0)
				if shell_count > 0:
					indices = range(shell_count)
				else:
					indices = (0, )
				for shell_index in indices:
					logging.debug(f"Exporting shell index {shell_index}")
					if b_me not in b_models:
						b_models.append((b_me, shell_index))
						wrapper = export_model(model_info, lod_coll, b_ob, b_me, bones_table, bounds, apply_transforms,
											   use_stock_normals_tangents, m_lod, shell_index, shell_count)
						wrapper.mesh.lod_index = lod_i
						wrapper.mesh.stream_info.pool_index = stream_index
					for b_mat in b_me.materials:
						logging.debug(f"Exporting material {b_mat.name}")
						if b_mat not in b_materials:
							b_materials.append(b_mat)
							export_material(model_info, b_mat)
							if "." in b_mat.name:
								messages.add(f"Material {b_mat.name} seems to be an unwanted duplication")
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
		export_bounds(bounds, model_info)
		# reset to original state
		for coll, state in zip(view_collections, view_states):
			coll.exclude = state
	# write ms2, backup should have been created earlier
	ms2.save(filepath)
	print(ms2)
	if found_scenes:
		messages.add(f"Finished MS2 export in {time.time() - start_time:.2f} seconds")
	else:
		mdl2_names = sorted(model_info_lut.keys())
		mdl2_names_str = '\n'.join(mdl2_names)
		raise AttributeError(
			f"Found no scenes matching MDL2s in MS2:\n"
			f"{mdl2_names_str}\n"
			f"Rename your scenes to match the MDL2s")
	return messages


