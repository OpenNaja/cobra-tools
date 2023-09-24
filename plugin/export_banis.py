import logging

import bpy
import mathutils
import numpy as np

from generated.formats.bani import BanisFile
from plugin.modules_export.armature import get_armature
from plugin.utils.matrix_util import get_scale_mat
from plugin.utils.object import get_bones_table


def get_fcurves_by_type(group, dtype):
	return [fcurve for fcurve in group.channels if fcurve.data_path.endswith(dtype)]


def get_groups_for_type(b_action, dtype):
	out = {}
	for group in b_action.groups:
		# if group.name in bones_lut:
		fcurves = get_fcurves_by_type(group, dtype)
		if fcurves:
			out[group] = fcurves
	return out


def get_local_bone(bone):
	if bone.parent:
		return bone.parent.matrix_local.inverted() @ bone.matrix_local
	return bone.matrix_local


def save(filepath=""):
	scene = bpy.context.scene
	bones_data = {}
	b_armature_ob = get_armature(scene)
	if not b_armature_ob:
		logging.warning(f"No armature was found in scene '{scene.name}' - did you delete it?")
		return "Failed, no armature"
	else:
		for bone in b_armature_ob.data.bones:
			bones_data[bone.name] = get_local_bone(bone)

	bones_table, p_bones = get_bones_table(b_armature_ob)
	banis = BanisFile()
	banis.num_anims = len(bpy.data.actions)
	banis.reset_field("anims")
	# per anim
	for b_action, bani in zip(bpy.data.actions, banis.anims):
		logging.info(f"Exporting {b_action.name}")
		# get fcurves
		# go by frame
		bani.name = b_action.name
		num_frames = int(round(b_action.frame_range[1] - b_action.frame_range[0]))
		bani.data.banis.pool_index = 0
		bani.data.animation_length = num_frames / scene.render.fps
		bani.keys = np.zeros(dtype=banis.dt_float, shape=(num_frames, len(bones_table)))
	# 	for bone_i, group in enumerate(pos_groups):
	# 		logging.info(f"Exporting loc '{group.name}'")
	# 		bonerestmat = bones_data[group.name]
	# 		if group.name == root_name:
	# 			bani.root_pos_bone = bone_i
	# 		fcurves = get_fcurves_by_type(group, "location")
	# 		fcurves_scale = get_fcurves_by_type(group, "scale")
	# 		for frame_i, frame in enumerate(k.pos_bones):
	# 			key = frame[bone_i]
	# 			# translation is stored relative to the parent
	# 			# whereas blender stores translation relative to the bone itself, not the parent
	# 			v = mathutils.Vector([fcu.evaluate(frame_i) for fcu in fcurves])
	# 			v = mathutils.Matrix.Translation(v)
	# 			# equivalent: multiply by rest rot and then add rest loc
	# 			v = bonerestmat @ v
	# 			v = sample_scale(fcurves_scale, frame_i, inverted=True) @ v
	# 			key.x, key.y, key.z = corrector.blender_bind_to_nif_bind(v).to_translation()
	# 	for bone_i, group in enumerate(ori_groups):
	# 		logging.info(f"Exporting rot '{group.name}'")
	# 		if group.name == root_name:
	# 			bani.root_ori_bone = bone_i
	# 		bonerestmat = bones_data[group.name]
	# 		fcurves = get_fcurves_by_type(group, "quaternion")
	# 		for frame_i, frame in enumerate(k.ori_bones):
	# 			key = frame[bone_i]
	# 			# sample frame
	# 			q_m = mathutils.Quaternion([fcu.evaluate(frame_i) for fcu in fcurves]).to_matrix().to_4x4()
	# 			# add local rest transform
	# 			final_m = bonerestmat @ q_m
	# 			final_m = corrector.blender_bind_to_nif_bind(final_m)
	# 			key.w, key.x, key.y, key.z = final_m.to_quaternion()
	# 	for bone_i, group in enumerate(scl_groups):
	# 		logging.info(f"Exporting scale '{group.name}'")
	# 		fcurves = get_fcurves_by_type(group, "scale")
	# 		for frame_i, frame in enumerate(k.scl_bones):
	# 			key = frame[bone_i]
	# 			scale_mat = sample_scale(fcurves, frame_i)
	# 			# needs axis correction, but appears to be stored relative to the animated bone's axes
	# 			scale_mat = corrector.blender_bind_to_nif_bind(scale_mat)
	# 			# swizzle
	# 			key.z, key.y, key.x = scale_mat.to_scale()
	# 		# no support for shear in blender bones, so set to neutral
	# 		# shear must not be 0.0
	# 		for frame in k.shr_bones:
	# 			key = frame[bone_i]
	# 			key.y = 1.0
	# 			key.x = 1.0
	# 	print(bani)
	# 	# print(bani.keys)
	# banis.header.banis_files_size = banis.banis_count * 16
	# banis.header.hash_block_size = len(target_names) * 4
	# banis.reset_field("name_buffer")
	# banis.name_buffer.bone_names[:] = sorted(target_names)
	# banis.name_buffer.bone_hashes[:] = [djb2(name.lower()) for name in banis.name_buffer.bone_names]
	banis.save(filepath)
	print(banis)
	return f"Finished banis export",
