import logging
import os

import bpy
import mathutils
import numpy as np

from generated.formats.base.basic import Ushort, Ubyte
from generated.formats.manis import ManisFile
from generated.formats.manis.compounds.ManiBlock import ManiBlock
from generated.formats.wsm.compounds.WsmHeader import WsmHeader
from modules.formats.shared import djb2
from plugin.modules_export.armature import assign_p_bone_indices, get_armatures_collections
from plugin.utils.matrix_util import bone_name_for_ovl, get_scale_mat
from plugin.utils.transforms import ManisCorrector

POS = "pos"
ORI = "ori"
SCL = "scl"
FLO = "float"
EUL = "euler"

root_name = "def_c_root_joint"
srb_name = "srb"


def store_pose_frame_info(b_obj, src_i, trg_i, bones_data, bone_channels, corrector):
	bpy.context.scene.frame_set(src_i)
	bpy.context.view_layer.update()
	for name, pbone in b_obj.pose.bones.items():
		# Get the final transform of the bone in its own local space...
		# then make it relative to the parent bone
		# transform is stored relative to the parent rest
		# whereas blender stores translation relative to the bone itself, not the parent
		matrix = bones_data[name] @ b_obj.convert_space(
			pose_bone=pbone, matrix=pbone.matrix, from_space='POSE', to_space='LOCAL')

		# loc
		v = sample_scale2(matrix, src_i, inverted=True) @ matrix
		bone_channels[name][POS][trg_i] = corrector.from_blender(v).to_translation()
		# rot
		final_m = corrector.from_blender(matrix)
		key = final_m.to_quaternion()
		# swizzle - w is stored last
		bone_channels[name][ORI][trg_i] = key.x, key.y, key.z, key.w
		if name == root_name:
			bone_channels[name][EUL][trg_i] = key.to_euler()
		# scale
		scale_mat = sample_scale2(matrix, src_i)
		# needs axis correction, but appears to be stored relative to the animated bone's axes
		scale_mat = corrector.from_blender(scale_mat)
		# swizzle
		key = scale_mat.to_scale()
		bone_channels[name][SCL][trg_i] = key.z, key.y, key.x


def needs_keyframes(keys):
	"""Checks a list of keys and returns True if temporal changes are detected"""
	if len(keys):
		# get the first key
		key0 = keys[0]
		# go over the channels
		for ch_i, ch_v in enumerate(key0):
			# do keys differ from first key?
			if not np.allclose(keys[:, ch_i], ch_v, rtol=1e-03, atol=1e-04, equal_nan=False):
				yield ch_i


def index_min_max(indices):
	if indices:
		return min(indices), max(indices)
	return 255, 0


def set_mani_info_counts(mani_info, bone_channels, bones_lut, m_dtype):
	# get count of all keyframed bones that appear in the bone index lut
	bone_names = [bone_name for bone_name, channels in bone_channels.items() if m_dtype in channels and bone_name in bones_lut]
	for s in (f"{m_dtype}_bone_count", f"{m_dtype}_bone_count_repeat", f"{m_dtype}_bone_count_related"):
		setattr(mani_info, s, len(bone_names))
	indices = [bones_lut[bone_name] for bone_name in bone_names]
	for s, v in zip((f"{m_dtype}_bone_min", f"{m_dtype}_bone_max"), index_min_max(indices)):
		setattr(mani_info, s, v)
	return bone_names, indices


def update_key_indices(k, m_dtype, b_names, indices, target_names, bone_names):
	m_names = [bone_name_for_ovl(name) for name in b_names]
	target_names.update(m_names)
	getattr(k, f"{m_dtype}_bones_names")[:] = m_names
	# map key data index to bone
	getattr(k, f"{m_dtype}_channel_to_bone")[:] = indices
	# map bones to key data index
	if indices:
		bone_0 = min(indices)
		bone_1 = max(indices) + 1
		key_lut = {name: i for i, name in enumerate(b_names)}
		getattr(k, f"{m_dtype}_bone_to_channel")[:] = [key_lut.get(name, 255) for name in bone_names[bone_0:bone_1]]


def get_local_bone(bone):
	if bone.parent:
		return bone.parent.matrix_local.inverted() @ bone.matrix_local
	return bone.matrix_local


def export_wsm(folder, mani_info, bone_name, bone_channels):
	wsm_name = f"{mani_info.name}_{bone_name}.wsm"
	wsm_path = os.path.join(folder, wsm_name)
	channels = bone_channels.get(bone_name)
	if channels:
		if POS in channels and ORI in channels:
			logging.info(f"Exporting {wsm_name} to {wsm_path}")
			wsm = WsmHeader(mani_info.context)
			wsm.duration = mani_info.duration
			wsm.frame_count = mani_info.frame_count
			wsm.unknowns[6] = 1.0
			wsm.reset_field("locs")
			wsm.reset_field("quats")
			for vec, data in zip(wsm.locs.data, bone_channels[bone_name][POS]):
				vec[:] = data
			for vec, data in zip(wsm.quats.data,bone_channels[bone_name][ORI]):
				vec[:] = data
			# print(wsm)
			with WsmHeader.to_xml_file(wsm, wsm_path):
				pass


def get_actions(b_ob):
	"""Returns a list of actions associated with b_ob"""
	actions = set()
	ad = b_ob.animation_data
	if ad:
		if ad.action:
			actions.add(ad.action)
		for t in ad.nla_tracks:
			for s in t.strips:
				actions.add(s.action)
	return list(actions)


def save(reporter, filepath="", per_armature=False):
	folder, manis_name = os.path.split(filepath)
	# manis_basename = os.path.splitext(filepath)[0]
	scene = bpy.context.scene
	bpy.ops.object.mode_set(mode='OBJECT')
	manis_datas = {}
	for b_armature_ob, mdl2_coll in get_armatures_collections(scene):
		logging.info(f"Exporting actions for {b_armature_ob.name}")
		if not b_armature_ob:
			logging.warning(f"No armature was found in MDL2 '{mdl2_coll.name}' - did you delete it?")
			continue
		# animation_data needn't be present on all armatures
		if not b_armature_ob.animation_data:
			logging.info(f"No animation data on '{b_armature_ob.name}'")
			continue
		# decide on exported name of manis file
		if per_armature:
			export_name = f"{b_armature_ob.name}_{manis_name}"
		else:
			export_name = manis_name
		# store data for actual export later
		if export_name not in manis_datas:
			manis_datas[export_name] = {}
		anim_map = manis_datas[export_name]
		if b_armature_ob not in anim_map:
			anim_map[b_armature_ob] = set()
		# store actions that are valid for this armature
		anim_map[b_armature_ob].update(get_actions(b_armature_ob))

	# export the actual manis
	for export_name, anim_map in manis_datas.items():
		manis = ManisFile()
		if scene.cobra.game == "Jurassic World Evolution":
			manis.version = 258
		elif scene.cobra.game == "Planet Zoo":
			manis.version = 260
		elif scene.cobra.game == "Jurassic World Evolution 2":
			manis.version = 262
		target_names = set()
		all_actions = [action for actions in anim_map.values() for action in actions]
		manis.mani_count = len(all_actions)
		manis.names[:] = [b_action.name for b_action in all_actions]
		manis.reset_field("mani_infos")
		manis.reset_field("keys_buffer")
		info_lut = {action: info for action, info in zip(all_actions, manis.mani_infos)}
		# export each armature and its actions to the corresponding mani_infos
		for b_armature_ob, actions in anim_map.items():
			mani_infos = [info_lut[action] for action in actions]
			export_armature_actions(b_armature_ob, actions, mani_infos, folder, scene, target_names)

		manis.header.mani_files_size = manis.mani_count * 16
		manis.header.hash_block_size = len(target_names) * 4
		manis.reset_field("name_buffer")
		manis.name_buffer.bone_names[:] = sorted(target_names)
		manis.name_buffer.bone_hashes[:] = [djb2(name.lower()) for name in manis.name_buffer.bone_names]
		filepath = os.path.join(folder, export_name)
		manis.save(filepath)
		reporter.show_info(f"Exported {export_name}")


def export_armature_actions(b_armature_ob, actions, mani_infos, folder, scene, target_names):
	corrector = ManisCorrector(False)
	bones_data = {bone.name: get_local_bone(bone) for bone in b_armature_ob.data.bones}
	try:
		bones_lut = {pose_bone.name: pose_bone["index"] for pose_bone in b_armature_ob.pose.bones}
	except:
		assign_p_bone_indices(b_armature_ob)
		bones_lut = {pose_bone.name: pose_bone["index"] for pose_bone in b_armature_ob.pose.bones}
	# raise AttributeError(
	# 	f"Some bones in {b_armature_ob.name} don't have the custom property 'index'.\n"
	# 	f"Assign a unique index to all bones by exporting the ms2 with 'Update Rig' checked.")
	bone_names = [pose_bone.name for pose_bone in sorted(b_armature_ob.pose.bones, key=lambda pb: pb["index"])]
	for b_action, mani_info in zip(actions, mani_infos):
		logging.info(f"Exporting {b_action.name}")
		mani_info.name = b_action.name
		first_frame, last_frame = b_action.frame_range
		mani_info.frame_count = int(round(last_frame) - round(first_frame)) + 1
		# index of last frame / fps
		mani_info.duration = (mani_info.frame_count - 1) / scene.render.fps
		mani_info.count_a = mani_info.count_b = 255
		mani_info.target_bone_count = len(b_armature_ob.pose.bones)

		# create arrays for loc, rot, scale keys
		bone_channels = {bone_name: {
			POS: np.empty((mani_info.frame_count, 3), float),
			ORI: np.empty((mani_info.frame_count, 4), float),
			SCL: np.empty((mani_info.frame_count, 3), float),
		} for bone_name in bone_names}
		# add euler for root motion
		if root_name in bone_channels:
			bone_channels[root_name][EUL] = np.empty((mani_info.frame_count, 3), float)
		# store pose data for b_action
		b_armature_ob.animation_data.action = b_action
		for trg_i, src_i in enumerate(range(int(first_frame), int(last_frame) + 1)):
			store_pose_frame_info(b_armature_ob, src_i, trg_i, bones_data, bone_channels, corrector)
		game = scene.cobra.game
		# export wsm before decimating bones
		if game == "Jurassic World Evolution 2":
			export_wsm(folder, mani_info, srb_name, bone_channels)
			# remove srb from bones_lut for JWE2, so it exported to wsm only
			bones_lut.pop(srb_name, None)

		# decide which channels to keyframe by determining if the keys are static
		for bone, channels in tuple(bone_channels.items()):
			for channel_id, keys in tuple(channels.items()):
				needed_axes = list(needs_keyframes(keys))
				if needed_axes:
					# copy root motion channels as floats
					if bone == root_name and channels:
						if channel_id == POS:
							add_root_float_keys(bone_channels, keys, needed_axes,
												("X Motion Track", "Y Motion Track", "Z Motion Track"))
							add_normed_float_keys(bone_channels, keys, needed_axes, "S Motion Track", game)
						if channel_id == EUL:
							add_root_float_keys(bone_channels, keys, needed_axes,
												("RotX Motion Track", "RotY Motion Track", "RotZ Motion Track"))
							add_normed_float_keys(bone_channels, keys, needed_axes, "T Motion Track", game)
					logging.debug(f"{bone} {channel_id} needs keys")
				else:
					channels.pop(channel_id)

		# print(bone_channels)
		pos_names, pos_indices = set_mani_info_counts(mani_info, bone_channels, bones_lut, POS)
		ori_names, ori_indices = set_mani_info_counts(mani_info, bone_channels, bones_lut, ORI)
		scl_names, scl_indices = set_mani_info_counts(mani_info, bone_channels, bones_lut, SCL)
		# floats are not necessarily per bone, so don't check for membership in bones_lut
		floats_names = [name for name, channels in bone_channels.items() if FLO in channels]
		target_names.update(floats_names)
		mani_info.float_count = len(floats_names)
		# mani_info.scl_bone_count_related = mani_info.scl_bone_count_repeat = 0
		# fill in the actual keys data
		bone_dtype = Ushort if mani_info.dtype.use_ushort else Ubyte
		mani_info.keys = ManiBlock(mani_info.context, mani_info, bone_dtype)
		k = mani_info.keys
		update_key_indices(k, POS, pos_names, pos_indices, target_names, bone_names)
		update_key_indices(k, ORI, ori_names, ori_indices, target_names, bone_names)
		update_key_indices(k, SCL, scl_names, scl_indices, target_names, bone_names)
		k.floats_names[:] = floats_names
		mani_info.root_pos_bone = mani_info.root_ori_bone = 255
		# todo maybe use key_indices lut to get root index
		# copy the keys
		for bone_i, name in enumerate(pos_names):
			if name == root_name:
				mani_info.root_pos_bone = bone_i
			k.pos_bones[:, bone_i] = bone_channels[name][POS]
		for bone_i, name in enumerate(ori_names):
			if name == root_name:
				mani_info.root_ori_bone = bone_i
			k.ori_bones[:, bone_i] = bone_channels[name][ORI]
		for bone_i, name in enumerate(scl_names):
			k.scl_bones[:, bone_i] = bone_channels[name][SCL]
		for bone_i, name in enumerate(floats_names):
			k.floats[:, bone_i] = bone_channels[name][FLO]
		# no support for shear in blender bones, so set to neutral - shear must not be 0.0
		k.shr_bones[:] = 1.0


def add_normed_float_keys(bone_channels, keys, needed_axes, float_name, game):
	if game == "Jurassic World Evolution":
		# S Motion Track ~ norm of X, Y, Z
		# T Motion Track ~ abs(RotY), probably also norm because usually only Y is used
		# make relative to first key
		val = np.array(keys[:, needed_axes])
		val -= val[0]
		# calculate the length of the vector for each frame
		bone_channels[float_name] = {}
		bone_channels[float_name][FLO] = np.linalg.norm(val, axis=1)


def add_root_float_keys(bone_channels, keys, needed_axes, names):
	for ch_i in needed_axes:
		float_name = names[ch_i]
		assert float_name not in bone_channels
		bone_channels[float_name] = {}
		bone_channels[float_name][FLO] = keys[:, ch_i]
		# make relative to first key
		bone_channels[float_name][FLO] -= keys[0, ch_i]


def sample_scale2(keymat, frame_i, inverted=False):
	v = keymat.to_scale()
	# this inversion is apparently not equivalent to a real matrix inversion
	if inverted:
		try:
			v = mathutils.Vector((1 / v.x, 1 / v.y, 1 / v.z))
		except:
			logging.exception(f"Could not invert {v} at {frame_i}")
	# v = mathutils.Matrix.Translation(v)
	scale_mat = get_scale_mat(v)
	return scale_mat
