import logging
import math
import os

import bpy
import mathutils
import numpy as np

from generated.formats.base.basic import Ushort, Ubyte
from generated.formats.manis import ManisFile
from generated.formats.manis.compounds.ManiBlock import ManiBlock
from generated.formats.manis.versions import set_game
from generated.formats.wsm.compounds.WsmHeader import WsmHeader
from modules.formats.shared import djb2
from plugin.utils.anim import c_map
from plugin.modules_export.armature import assign_p_bone_indices, get_armatures_collections
from plugin.modules_import.anim import get_rna_path
from plugin.utils.blender_util import bone_name_for_ovl, get_scale_mat
from plugin.utils.transforms import ManisCorrector

POS = "pos"
ORI = "ori"
SCL = "scl"
FLO = "float"
EUL = "euler"

root_name = "def_c_root_joint"
srb_name = "srb"


def store_pose_frame_info(b_ob, src_i, trg_i, bones_data, channel_storage, corrector, cam_corr):
	bpy.context.scene.frame_set(src_i)
	bpy.context.view_layer.update()
	if b_ob.type == "CAMERA":
		store_transform_data(channel_storage, corrector, b_ob.matrix_local, "camera_joint", src_i, trg_i, cam_corr)
	elif b_ob.type == "ARMATURE":
		for name, p_bone in b_ob.pose.bones.items():
			# Get the final transform of the bone in its own local space...
			# then make it relative to the parent bone
			# transform is stored relative to the parent rest
			# whereas blender stores translation relative to the bone itself, not the parent
			matrix = bones_data[name] @ b_ob.convert_space(
				pose_bone=p_bone, matrix=p_bone.matrix, from_space='POSE', to_space='LOCAL')
			store_transform_data(channel_storage, corrector, matrix, name, src_i, trg_i, cam_corr)


def store_transform_data(channel_storage, corrector, matrix, name, src_i, trg_i, cam_corr):
	# loc
	v = sample_scale2(matrix, src_i, inverted=True) @ matrix
	channel_storage[name][POS][trg_i] = corrector.from_blender(v).to_translation()
	# rot
	final_m = corrector.from_blender(matrix)
	key = final_m.to_quaternion()
	if cam_corr is not None:
		out = mathutils.Quaternion(cam_corr)
		key.rotate(out)
		key = mathutils.Quaternion((key.x, -key.y, key.w, -key.z))
	# swizzle - w is stored last
	channel_storage[name][ORI][trg_i] = key.x, key.y, key.z, key.w
	if name == root_name:
		channel_storage[name][EUL][trg_i] = key.to_euler()
	# scale
	scale_mat = sample_scale2(matrix, src_i)
	# needs axis correction, but appears to be stored relative to the animated bone's axes
	scale_mat = corrector.from_blender(scale_mat)
	# swizzle
	key = scale_mat.to_scale()
	channel_storage[name][SCL][trg_i] = key.z, key.y, key.x


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


def set_mani_info_counts(mani_info, channel_storage, bones_lut, m_dtype):
	# get count of all keyframed bones that appear in the bone index lut
	bone_names = [bone_name for bone_name, channels in channel_storage.items() if m_dtype in channels and bone_name in bones_lut]
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


def export_wsm(folder, mani_info, bone_name, channel_storage):
	wsm_name = f"{mani_info.name}_{bone_name}.wsm"
	wsm_path = os.path.join(folder, wsm_name)
	channels = channel_storage.get(bone_name)
	if channels:
		if POS in channels and ORI in channels:
			logging.info(f"Exporting {wsm_name} to {wsm_path}")
			wsm = WsmHeader(mani_info.context)
			wsm.duration = mani_info.duration
			wsm.frame_count = mani_info.frame_count
			wsm.unknowns[6] = 1.0
			wsm.reset_field("locs")
			wsm.reset_field("quats")
			for vec, data in zip(wsm.locs.data, channel_storage[bone_name][POS]):
				vec[:] = data
			for vec, data in zip(wsm.quats.data,channel_storage[bone_name][ORI]):
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
	export_objects = get_armatures_collections(scene)
	for b_ob in scene.objects:
		if b_ob.type == "CAMERA":
			export_objects.append((b_ob, scene.collection))
	for b_ob, mdl2_coll in export_objects:
		if not b_ob:
			logging.warning(f"No armature was found in MDL2 '{mdl2_coll.name}' - did you delete it?")
			continue
		logging.info(f"Exporting actions for {b_ob.name}")
		# animation_data needn't be present on all armatures
		if not b_ob.animation_data:
			logging.info(f"No animation data on '{b_ob.name}'")
			continue
		# decide on exported name of manis file
		if per_armature:
			export_name = f"{b_ob.name}_{manis_name}"
		else:
			export_name = manis_name
		# store data for actual export later
		if export_name not in manis_datas:
			manis_datas[export_name] = {}
		anim_map = manis_datas[export_name]
		if b_ob not in anim_map:
			anim_map[b_ob] = set()
		# store actions that are valid for this armature
		anim_map[b_ob].update(get_actions(b_ob))

	# export the actual manis
	for export_name, anim_map in manis_datas.items():
		manis = ManisFile()
		set_game(manis, scene.cobra.game)
		target_names = set()
		all_actions = [action for actions in anim_map.values() for action in actions]
		manis.mani_count = len(all_actions)
		manis.names[:] = [b_action.name for b_action in all_actions]
		manis.reset_field("mani_infos")
		manis.reset_field("keys_buffer")
		info_lut = {action: info for action, info in zip(all_actions, manis.mani_infos)}
		# export each armature and its actions to the corresponding mani_infos
		for b_ob, actions in anim_map.items():
			mani_infos = [info_lut[action] for action in actions]
			export_actions(b_ob, actions, mani_infos, folder, scene, target_names)

		manis.header.mani_files_size = manis.mani_count * 16
		manis.header.hash_block_size = len(target_names) * 4
		manis.reset_field("name_buffer")
		manis.name_buffer.bone_names[:] = sorted(target_names)
		manis.name_buffer.bone_hashes[:] = [djb2(name.lower()) for name in manis.name_buffer.bone_names]
		filepath = os.path.join(folder, export_name)
		manis.save(filepath)
		reporter.show_info(f"Exported {export_name}")


def export_actions(b_ob, actions, mani_infos, folder, scene, target_names):
	corrector = ManisCorrector(False)
	game = scene.cobra.game
	if b_ob.type == "ARMATURE":
		bones_data = {bone.name: get_local_bone(bone) for bone in b_ob.data.bones}
		assign_p_bone_indices(b_ob)
		bones_lut = {p_bone.name: p_bone["index"] for p_bone in b_ob.pose.bones}
		cam_corr = None
	else:
		bones_lut = {"unk1": 0, "camera_joint": 1, "unk2": 2}  # camera_joint is index 1, count is 3
		bones_data = {name: mathutils.Matrix().to_4x4() for name in bones_lut}
		cam_corr = mathutils.Euler((math.radians(90), 0, math.radians(-90))).to_quaternion()
		cam_corr.invert()
	bone_names = [n for n, i in sorted(bones_lut.items(), key=lambda kv: kv[1])]
	for b_action, mani_info in zip(actions, mani_infos):
		logging.info(f"Exporting {b_action.name}")
		mani_info.name = b_action.name
		first_frame, last_frame = b_action.frame_range
		first_frame = int(first_frame)
		last_frame = int(last_frame) + 1
		mani_info.frame_count = last_frame - first_frame
		# index of last frame / fps
		mani_info.duration = (mani_info.frame_count - 1) / scene.render.fps
		mani_info.count_a = mani_info.count_b = 255
		mani_info.target_bone_count = len(bones_data)

		# create arrays for loc, rot, scale keys
		channel_storage = {bone_name: {
			POS: np.zeros((mani_info.frame_count, 3), float),
			ORI: np.zeros((mani_info.frame_count, 4), float),
			SCL: np.zeros((mani_info.frame_count, 3), float),
		} for bone_name in bone_names}
		# add euler for root motion
		if root_name in channel_storage:
			channel_storage[root_name][EUL] = np.zeros((mani_info.frame_count, 3), float)
		# store pose data for b_action
		b_ob.animation_data.action = b_action
		for trg_i, src_i in enumerate(range(first_frame, last_frame)):
			store_pose_frame_info(b_ob, src_i, trg_i, bones_data, channel_storage, corrector, cam_corr)
		# export wsm before decimating bones
		if game == "Jurassic World Evolution 2":
			# todo identify additional condition for this; it is not motionextracted vs notmotionextracted
			export_wsm(folder, mani_info, srb_name, channel_storage)
			# remove srb from bones_lut for JWE2, so it exported to wsm only
			bones_lut.pop(srb_name, None)

		# decide which channels to keyframe by determining if the keys are static
		for bone, channels in tuple(channel_storage.items()):
			for channel_id, keys in tuple(channels.items()):
				needed_axes = list(needs_keyframes(keys))
				if needed_axes:
					# copy root motion channels as floats
					if bone == root_name and channels:
						# copy to avoid modifying the original keys data
						keys = keys.copy()
						if channel_id == POS:
							add_root_float_keys(channel_storage, keys, needed_axes,
												("X Motion Track", "Y Motion Track", "Z Motion Track"))
							add_normed_float_keys(channel_storage, keys, needed_axes, "S Motion Track", game)
						if channel_id == EUL:
							add_root_float_keys(channel_storage, keys, needed_axes,
												("RotX Motion Track", "RotY Motion Track", "RotZ Motion Track"))
							add_normed_float_keys(channel_storage, keys, needed_axes, "T Motion Track", game)
					logging.debug(f"{bone} {channel_id} needs keys")
				else:
					# no need to keyframe this bone, discard it
					channels.pop(channel_id)
		# export constraints as float keys
		if b_ob.type == "ARMATURE":
			# find constraints that qualify
			constraint_bones = {}
			for p_bone in b_ob.pose.bones:
				for const in p_bone.constraints:
					for c_suffix, c_type, create, limits in c_map:
						if const.type == c_type:
							rna_path = get_rna_path("influence", p_bone.name, None, const.name)
							constraint_bones[rna_path] = (c_suffix, limits, bone_name_for_ovl(p_bone.name))
			# export fcurves for those constraints
			for fcu in b_action.fcurves:
				if fcu.data_path in constraint_bones and fcu.array_index == 0:
					c_suffix, limits, m_name = constraint_bones[fcu.data_path]
					keys = sample_fcu(fcu, first_frame, last_frame, mani_info)
					if limits:
						l_min, l_max = limits
						keys *= (l_max - l_min)
						keys += l_min
					float_name = f"{m_name}.{c_suffix}"
					channel_storage[float_name] = {FLO: keys}
		
		if "_camera" in b_action.name:
			# FOV is in the camera data action, which has to be queried and looped
			b_data_action = bpy.data.actions.get(f"{b_action.name}_Data", None)
			if b_data_action:
				for fcu in b_data_action.fcurves:
					if fcu.data_path == get_rna_path("lens"):
						keys = sample_fcu(fcu, first_frame, last_frame, mani_info)
						# FOV = 2*arctan(w / (2*focal_len))
						# original sensor width
						keys = 2 * np.arctan(36 / (2*keys))
						channel_storage["CameraFOV"] = {FLO: keys}

		# print(channel_storage)
		pos_names, pos_indices = set_mani_info_counts(mani_info, channel_storage, bones_lut, POS)
		ori_names, ori_indices = set_mani_info_counts(mani_info, channel_storage, bones_lut, ORI)
		scl_names, scl_indices = set_mani_info_counts(mani_info, channel_storage, bones_lut, SCL)
		# floats are not necessarily per bone, so don't check for membership in bones_lut
		floats_names = [name for name, channels in channel_storage.items() if FLO in channels]
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
		# copy the keys and set root bone indices
		mani_info.root_pos_bone = mani_info.root_ori_bone = 255
		for bone_i, name in enumerate(pos_names):
			if name == root_name:
				mani_info.root_pos_bone = bone_i
			k.pos_bones[:, bone_i] = channel_storage[name][POS]
		for bone_i, name in enumerate(ori_names):
			if name == root_name:
				mani_info.root_ori_bone = bone_i
			k.ori_bones[:, bone_i] = channel_storage[name][ORI]
		for bone_i, name in enumerate(scl_names):
			k.scl_bones[:, bone_i] = channel_storage[name][SCL]
		for bone_i, name in enumerate(floats_names):
			k.floats[:, bone_i] = channel_storage[name][FLO]
		# no support for shear in blender bones, so set to neutral - shear must not be 0.0
		k.shr_bones[:] = 1.0


def sample_fcu(fcu, first_frame, last_frame, mani_info):
	keys = np.empty(mani_info.frame_count)
	keys[:] = [fcu.evaluate(i) for i in range(first_frame, last_frame)]
	return keys


def add_normed_float_keys(channel_storage, keys, needed_axes, float_name, game):
	if game == "Jurassic World Evolution":
		# S Motion Track ~ norm of X, Y, Z
		# T Motion Track ~ abs(RotY), probably also norm because usually only Y is used
		# make relative to first key
		val = np.array(keys[:, needed_axes])
		val -= val[0]
		# calculate the length of the vector for each frame
		channel_storage[float_name] = {}
		channel_storage[float_name][FLO] = np.linalg.norm(val, axis=1)


def add_root_float_keys(channel_storage, keys, needed_axes, names):
	for ch_i in needed_axes:
		float_name = names[ch_i]
		assert float_name not in channel_storage
		channel_storage[float_name] = {}
		channel_storage[float_name][FLO] = keys[:, ch_i]
		# make relative to first key
		channel_storage[float_name][FLO] -= keys[0, ch_i]


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
