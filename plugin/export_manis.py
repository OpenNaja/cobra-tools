import logging

import bpy
import mathutils
from bpy_extras.io_utils import axis_conversion

from generated.formats.manis import ManisFile
from generated.formats.manis.compounds.ManiBlock import ManiBlock
from modules.formats.shared import djb2
from plugin.modules_export.armature import get_armature
from plugin.utils.matrix_util import bone_name_for_ovl
from plugin.utils.transforms import ManisCorrector


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


def index_min_max(indices):
	if indices:
		return min(indices), max(indices)
	return 255, 0


def set_mani_info_counts(mani_info, b_action, bones_lut, m_dtype, b_dtype):
	groups = get_groups_for_type(b_action, b_dtype)
	count = len(groups)
	for s in (f"{m_dtype}_bone_count", f"{m_dtype}_bone_count_repeat", f"{m_dtype}_bone_count_related"):
		setattr(mani_info, s, count)
	indices = [bones_lut[group.name] for group in groups]
	for s, v in zip((f"{m_dtype}_bone_min", f"{m_dtype}_bone_max"), index_min_max(indices)):
		setattr(mani_info, s, v)
	return groups, indices


def update_key_indices(k, m_dtype, groups, indices, target_names, bone_names):
	b_names = [group.name for group in groups]
	m_names = [bone_name_for_ovl(name) for name in b_names]
	target_names.update(m_names)
	getattr(k, f"{m_dtype}_bones")[:] = m_names
	# map key data index to bone
	getattr(k, f"{m_dtype}_bones_p")[:] = indices
	# map bones to key data index
	if indices:
		bone_0 = min(indices)
		bone_1 = max(indices) + 1
		key_lut = {name: i for i, name in enumerate(b_names)}
		getattr(k, f"{m_dtype}_bones_delta")[:] = [key_lut.get(name, 255) for name in bone_names[bone_0:bone_1]]


def get_local_bone(bone):
	if bone.parent:
		return bone.parent.matrix_local.inverted() @ bone.matrix_local
	return bone.matrix_local


def get_scale_mat(scale_vec):
	scale_matrix_x2 = mathutils.Matrix.Scale(scale_vec.x, 4, (1.0, 0.0, 0.0))
	scale_matrix_y2 = mathutils.Matrix.Scale(scale_vec.y, 4, (0.0, 1.0, 0.0))
	scale_matrix_z2 = mathutils.Matrix.Scale(scale_vec.z, 4, (0.0, 0.0, 1.0))
	return scale_matrix_x2 @ scale_matrix_y2 @ scale_matrix_z2


def save(filepath=""):
	scene = bpy.context.scene
	bones_data = {}
	b_armature_ob = get_armature(scene)
	if not b_armature_ob:
		logging.warning(f"No armature was found in scene '{scene.name}' - did you delete it?")
	else:
		for bone in b_armature_ob.data.bones:
			bones_data[bone.name] = get_local_bone(bone)

	corrector = ManisCorrector(False)
	mani = ManisFile()
	# hardcode for PZ for now, but it does not make a difference outside of compressed keys
	mani.version = 260
	target_names = set()
	bones_lut = {pose_bone.name: pose_bone["index"] for pose_bone in b_armature_ob.pose.bones}
	bone_names = [pose_bone.name for pose_bone in sorted(b_armature_ob.pose.bones, key=lambda pb: pb["index"])]
	action_names = [b_action.name for b_action in bpy.data.actions]
	mani.mani_count = len(action_names)
	mani.names[:] = action_names
	mani.reset_field("mani_infos")
	mani.reset_field("keys_buffer")
	# scale_corr = axis_conversion("X", "Y").to_4x4().inverted()
	# scale_corr = mathutils.Matrix((
	# 	(0.0000, 1.0000, 0.0000, 0.0000),
	# 	(0.0000, 0.0000, 1.0000, 0.0000),
	# 	(1.0000, 0.0000, 0.0000, 0.0000),
	# 	(0.0000, 0.0000, 0.0000, 1.0000)))
	# scale_corr = mathutils.Matrix((
	# 	(0.0000, 1.0000, 0.0000, 0.0000),
	# 	(1.0000, 0.0000, 0.0000, 0.0000),
	# 	(0.0000, 0.0000, 1.0000, 0.0000),
	# 	(0.0000, 0.0000, 0.0000, 1.0000)))
	# print(scale_corr)
	for b_action, mani_info in zip(bpy.data.actions, mani.mani_infos):
		logging.info(f"Exporting {b_action.name}")
		mani_info.frame_count = int(round(b_action.frame_range[1] - b_action.frame_range[0]))
		# assume fps = 30
		# mani_info.duration = mani_info.frame_count / scene.render.fps
		mani_info.duration = mani_info.frame_count / 30.0
		mani_info.count_a = mani_info.count_b = 255
		mani_info.target_bone_count = len(b_armature_ob.pose.bones)
		pos_groups, pos_indices = set_mani_info_counts(mani_info, b_action, bones_lut, "pos", "location")
		ori_groups, ori_indices = set_mani_info_counts(mani_info, b_action, bones_lut, "ori", "quaternion")
		scl_groups, scl_indices = set_mani_info_counts(mani_info, b_action, bones_lut, "scl", "scale")
		# mani_info.scl_bone_count_related = mani_info.scl_bone_count_repeat = 0
		floats = []
		print(mani_info)
		mani_info.keys = ManiBlock(mani_info.context, mani_info)
		k = mani_info.keys
		update_key_indices(k, "pos", pos_groups, pos_indices, target_names, bone_names)
		update_key_indices(k, "ori", ori_groups, ori_indices, target_names, bone_names)
		update_key_indices(k, "scl", scl_groups, scl_indices, target_names, bone_names)
		for bone_i, group in enumerate(pos_groups):
			logging.info(f"Exporting loc '{group.name}'")
			bonerestmat = bones_data[group.name]
			fcurves = get_fcurves_by_type(group, "location")
			for frame_i, frame in enumerate(k.key_data.pos_bones):
				key = frame[bone_i]
				# translation is stored relative to the parent
				# whereas blender stores translation relative to the bone itself, not the parent
				v = mathutils.Vector([fcu.evaluate(frame_i) for fcu in fcurves])
				v = mathutils.Matrix.Translation(v)
				# equivalent: multiply by rest rot and then add rest loc
				v = bonerestmat @ v
				key.x, key.y, key.z = corrector.blender_bind_to_nif_bind(v).to_translation()
		for bone_i, group in enumerate(ori_groups):
			logging.info(f"Exporting rot '{group.name}'")
			bonerestmat = bones_data[group.name]
			fcurves = get_fcurves_by_type(group, "quaternion")
			for frame_i, frame in enumerate(k.key_data.ori_bones):
				key = frame[bone_i]
				# sample frame
				q_m = mathutils.Quaternion([fcu.evaluate(frame_i) for fcu in fcurves]).to_matrix().to_4x4()
				# add local rest transform
				final_m = bonerestmat @ q_m
				final_m = corrector.blender_bind_to_nif_bind(final_m)
				key.w, key.x, key.y, key.z = final_m.to_quaternion()
		for bone_i, group in enumerate(scl_groups):
			logging.info(f"Exporting scale '{group.name}'")
			fcurves = get_fcurves_by_type(group, "scale")
			for frame_i, frame in enumerate(k.key_data.scl_bones):
				# found in DLA SpaceMountain animations.manisetd740d135
				key = frame[bone_i]
				v = mathutils.Vector([fcu.evaluate(frame_i) for fcu in fcurves])
				# v = mathutils.Matrix.Translation(v)
				scale_mat = get_scale_mat(v)
				# needs correction, and possibly relative to bind
				# not sure about the right correction
				# scale_mat = scale_mat @ scale_corr
				scale_mat = corrector.blender_bind_to_nif_bind(scale_mat)
				key.x, key.y, key.z = scale_mat.to_scale()
			# no support for shear in blender bones, so set to neutral
			# shear must not be 0.0
			for frame in k.key_data.shr_bones:
				key = frame[bone_i]
				key.y = 1.0
				key.x = 1.0
		print(mani_info.keys)
	mani.header.mani_files_size = mani.mani_count * 16
	mani.header.hash_block_size = len(target_names) * 4
	mani.reset_field("name_buffer")
	mani.name_buffer.bone_names[:] = sorted(target_names)
	mani.name_buffer.bone_hashes[:] = [djb2(name.lower()) for name in mani.name_buffer.bone_names]
	mani.save(filepath)
	return f"Finished manis export",
