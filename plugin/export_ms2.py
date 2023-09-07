import logging
import math
import os
import time

import bpy
import mathutils
import numpy as np

from generated.formats.ms2.compounds.LodInfo import LodInfo
from generated.formats.ms2.compounds.Object import Object
from generated.formats.ms2 import Ms2File, is_jwe2
from plugin.modules_export.armature import get_armature, export_bones_custom
from plugin.modules_export.collision import export_bounds, get_bounds
from plugin.modules_export.geometry import export_model
from plugin.modules_export.material import export_material
from plugin.modules_import.armature import get_bone_names
from plugin.utils.object import has_objects_in_scene, get_property
from plugin.utils.shell import get_collection
from source.formats.ms2.compounds.packing_utils import PACKEDVEC_MAX


def get_pack_base(b_obs):
	"""Detect a suitable pack_base value depending on the bounds of b_obs"""
	# todo JWE2 perhaps supports unique pack_base per vert_chunk
	bounds = [ob.bound_box for ob in b_obs]
	bounds_max, bounds_min = get_bounds(bounds)
	coord_min = np.min(bounds_min)
	coord_max = np.max(bounds_max)
	for pack_base in [float(2 ** x) for x in range(1, 16)]:
		if -pack_base < coord_min and coord_max < pack_base:
			return pack_base


def save(filepath='', apply_transforms=False, update_rig=False, use_stock_normals_tangents=False):
	messages = set()
	start_time = time.time()

	logging.info(f"Exporting {filepath} into export subfolder...")
	if not os.path.isfile(filepath):
		raise FileNotFoundError(f"{filepath} does not exist. You must open an existing ms2 file for exporting.")

	old_dir, name = os.path.split(os.path.normpath(filepath))
	exp_dir = os.path.join(old_dir, "export")
	os.makedirs(exp_dir, exist_ok=True)
	export_path = os.path.join(exp_dir, name)
	ms2 = Ms2File()
	ms2.load(filepath)
	ms2.read_editable = True
	ms2.clear()

	model_info_lut = {mdl2_name: model_info for mdl2_name, model_info in zip(ms2.mdl_2_names, ms2.model_infos)}
	for scene in bpy.data.scenes:
		if scene.name not in model_info_lut:
			logging.warning(f"Scene '{scene.name}' was not found in the MS2 file, skipping")
			continue
		logging.debug(f"Exporting scene {scene.name}")

		# make active scene
		bpy.context.window.scene = scene
		model_info = model_info_lut[scene.name]
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
			lod_group_name = f"{scene.name}_LOD{lod_i}"
			lod_coll = get_collection(lod_group_name)
			if not lod_coll:
				break
			lod_collections.append(lod_coll)

		model_info.pack_base = get_pack_base(lod_collections[0].objects)
		model_info.precision = model_info.pack_base / PACKEDVEC_MAX
		# logging.debug(f"chose pack_base = {model_info.pack_base} precision = {model_info.precision}")
		for lod_i, lod_coll in enumerate(lod_collections):
			m_lod = LodInfo(ms2.context)
			m_lod.distance = math.pow(30 + 15 * lod_i, 2)
			m_lod.first_object_index = len(model_info.model.objects)
			m_lod.meshes = []
			m_lod.objects = []
			model_info.model.lods.append(m_lod)
			for b_ob in lod_coll.objects:
				logging.debug(f"Exporting b_ob {b_ob.name}")
				b_me = b_ob.data
				m_lod.stream_index = get_property(b_me, "stream")
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
					for b_mat in b_me.materials:
						logging.debug(f"Exporting material {b_mat.name}")
						if b_mat not in b_materials:
							b_materials.append(b_mat)
							export_material(model_info, b_mat)
							if "." in b_mat.name:
								messages.add(f"Material {b_mat.name} seems to be an unwanted duplication!")
						# create one unique mesh per material
						m_ob = Object(ms2.context)
						m_ob.mesh_index = b_models.index((b_me, shell_index))
						m_ob.material_index = b_materials.index(b_mat)

						model_info.model.objects.append(m_ob)
						wrapper = model_info.model.meshes[m_ob.mesh_index]
						m_lod.meshes.append(wrapper)
						if wrapper.context.version >= 52:
							logging.debug(f"Setting chunk material indices")
							for tri_chunk in wrapper.mesh.tri_chunks:
								tri_chunk.material_index = m_ob.material_index
						m_lod.objects.append(m_ob)
			m_lod.last_object_index = len(model_info.model.objects)

		export_bounds(bounds, model_info)

	# write modified ms2
	ms2.save(export_path)

	messages.add(f"Finished MS2 export in {time.time() - start_time:.2f} seconds")
	return messages


