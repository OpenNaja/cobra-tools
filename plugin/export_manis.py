import logging
import math
import os

import bpy
import mathutils
import numpy as np

from generated.formats.base.basic import Ushort, Ubyte
from generated.formats.manis import ManisFile, POS, ORI, SCL, FLO, EUL, root_name, srb_name
from generated.formats.manis.compounds.ManiBlock import ManiBlock
from generated.formats.manis.versions import set_game
from generated.formats.wsm.compounds.WsmHeader import WsmHeader
from plugin.utils.anim import c_map
from plugin.modules_export.armature import assign_p_bone_indices, get_armatures_collections, get_bone_matrices
from plugin.modules_import.anim import get_rna_path
from plugin.utils.blender_util import bone_name_for_ovl, get_scale_mat
from plugin.utils.object import get_property
from plugin.utils.transforms import ManisCorrector


def store_pose_frame_info(b_ob, src_frame, trg_frame, bones_data, channel_storage, corrector, cam_corr):
	bpy.context.scene.frame_set(src_frame)
	bpy.context.view_layer.update()
	if b_ob.type == "CAMERA":
		store_transform_data(channel_storage, corrector, b_ob.matrix_local, "camera_joint", src_frame, trg_frame, cam_corr)
	elif b_ob.type == "ARMATURE":
		for b_name, p_bone in b_ob.pose.bones.items():
			m_name = bone_name_for_ovl(b_name)
			# Get the final transform of the bone in its own local space...
			# then make it relative to the parent bone
			# transform is stored relative to the parent rest
			# whereas blender stores translation relative to the bone itself, not the parent
			matrix = bones_data[m_name] @ b_ob.convert_space(
				pose_bone=p_bone, matrix=p_bone.matrix, from_space='POSE', to_space='LOCAL')
			store_transform_data(channel_storage, corrector, matrix, m_name, src_frame, trg_frame, cam_corr)


def store_transform_data(channel_storage, corrector, matrix, name, src_frame, trg_frame, cam_corr):
	# loc
	v = sample_scale2(matrix, src_frame, inverted=True) @ matrix
	channel_storage[name][POS][trg_frame] = corrector.from_blender(v).to_translation()
	# rot
	final_m = corrector.from_blender(matrix)
	key = final_m.to_quaternion()
	if cam_corr is not None:
		out = mathutils.Quaternion(cam_corr)
		key.rotate(out)
		key = mathutils.Quaternion((key.x, -key.y, key.w, -key.z))
	# swizzle - w is stored last
	channel_storage[name][ORI][trg_frame] = key.x, key.y, key.z, key.w
	if name == srb_name:
		channel_storage[name][EUL][trg_frame] = key.to_euler()
	# scale
	scale_mat = sample_scale2(matrix, src_frame)
	# needs axis correction, but appears to be stored relative to the animated bone's axes
	scale_mat = corrector.from_blender(scale_mat)
	# swizzle
	key = scale_mat.to_scale()
	channel_storage[name][SCL][trg_frame] = key.z, key.y, key.x


def reasonably_close(a, b):
	return np.allclose(a, b, rtol=1e-04, atol=1e-06, equal_nan=False)


def needs_keyframes(keys):
	"""Checks an array of keys and yields the indices that have temporal changes"""
	if len(keys):
		# get the first key
		key0 = keys[0]
		# go over the channels
		for ch_i, ch_v in enumerate(key0):
			# do keys differ from first key?
			if not reasonably_close(keys[:, ch_i], ch_v):
				yield ch_i


def set_mani_info_counts(mani_info, channel_storage, m_dtype):
	# get count of all keyframed bones that appear in the bone index lut
	m_bone_names = [bone_name for bone_name, channels in channel_storage.items() if m_dtype in channels and bone_name in mani_info.context.bones_lut]
	for s in (f"{m_dtype}_bone_count", f"{m_dtype}_bone_count_repeat", f"{m_dtype}_bone_count_related"):
		setattr(mani_info, s, len(m_bone_names))
	return m_bone_names


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
			for vec, data in zip(wsm.quats.data, channel_storage[bone_name][ORI]):
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
				if s.action:
					actions.add(s.action)
	return list(actions)


def save(reporter, filepath="", per_armature=False):
	folder, manis_name = os.path.split(filepath)
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
		all_actions = [action for actions in anim_map.values() for action in actions]
		manis.mani_count = len(all_actions)
		manis.reset_field("mani_infos")
		manis.reset_field("keys_buffer")
		info_lut = {action: mani_info for action, mani_info in zip(all_actions, manis.mani_infos)}
		# export each armature and its actions to the corresponding mani_infos
		for b_ob, actions in anim_map.items():
			mani_infos = [info_lut[action] for action in actions]
			export_actions(b_ob, actions, manis, mani_infos, folder, scene)

		filepath = os.path.join(folder, export_name)
		manis.save(filepath)
		reporter.show_info(f"Exported {export_name}")

def needs_wsm(bone, game):
	# todo identify additional condition for this; it is not motionextracted vs notmotionextracted
	return bone == srb_name and game == "Jurassic World Evolution 2"

def export_actions(b_ob, actions, manis, mani_infos, folder, scene):
	corrector = ManisCorrector(False)
	game = scene.cobra.game
	bones_data = {}
	rest_data = {}
	if b_ob.type == "ARMATURE":
		for b_bone in b_ob.data.bones:
			m_name = bone_name_for_ovl(b_bone.name)
			mat_local, mat_local_to_parent = get_bone_matrices(b_bone, corrector)
			bones_data[m_name] = get_local_bone(b_bone)
			fill_in_rest_data(m_name, mat_local_to_parent, rest_data)
		assign_p_bone_indices(b_ob)
		manis.context.bones_lut = {bone_name_for_ovl(p_bone.name): p_bone["index"] for p_bone in b_ob.pose.bones}
		cam_corr = None
	else:
		manis.context.bones_lut = {"unk1": 0, "camera_joint": 1, "unk2": 2}  # camera_joint is index 1, count is 3
		for m_name in manis.context.bones_lut:
			mat_local_to_parent = mathutils.Matrix().to_4x4()
			bones_data[m_name] = mat_local_to_parent
			fill_in_rest_data(m_name, mat_local_to_parent, rest_data)
		cam_corr = mathutils.Euler((math.radians(90), 0, math.radians(-90))).to_quaternion()
		cam_corr.invert()

	# sort bones by their index
	m_bone_names = manis.sorted_ms2_bone_names
	for b_action, mani_info in zip(actions, mani_infos):
		logging.info(f"Exporting {b_action.name}")
		mani_info.name = b_action.name
		# update ovs name
		manis.stream = get_property(b_action, "stream", default="")
		first_frame, last_frame = b_action.frame_range
		first_frame = int(first_frame)
		last_frame = int(last_frame) + 1
		mani_info.frame_count = last_frame - first_frame
		# index of last frame / fps
		mani_info.duration = (mani_info.frame_count - 1) / scene.render.fps
		mani_info.count_a = mani_info.count_b = 255
		mani_info.target_bone_count = len(bones_data)

		# create arrays for loc, rot, scale keys
		channel_storage = {m_bone_name: {
			POS: np.zeros((mani_info.frame_count, 3), float),
			ORI: np.zeros((mani_info.frame_count, 4), float),
			SCL: np.zeros((mani_info.frame_count, 3), float),
		} for m_bone_name in m_bone_names}
		# add euler for root motion
		if srb_name in channel_storage:
			channel_storage[srb_name][EUL] = np.zeros((mani_info.frame_count, 3), float)
		# store pose data for b_action
		b_ob.animation_data.action = b_action
		for trg_frame, src_frame in enumerate(range(first_frame, last_frame)):
			store_pose_frame_info(b_ob, src_frame, trg_frame, bones_data, channel_storage, corrector, cam_corr)

		# decide which channels to keyframe by determining if the keys are static
		for bone, channels in tuple(channel_storage.items()):
			# export wsm before decimating bones
			if needs_wsm(bone, game):
				export_wsm(folder, mani_info, srb_name, channel_storage)
			for channel_id, keys in tuple(channels.items()):
				needed_axes = list(needs_keyframes(keys))
				# copy root motion channels as floats
				if bone == srb_name:
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
					# delete srb bone from mani; the float channels created before are needed
					if needs_wsm(bone, game):
						channels.pop(channel_id)
						continue
				# decimate channels
				if not needed_axes or reasonably_close(keys[0], rest_data[bone][channel_id]):
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
		pos_names = set_mani_info_counts(mani_info, channel_storage, POS)
		ori_names = set_mani_info_counts(mani_info, channel_storage, ORI)
		scl_names = set_mani_info_counts(mani_info, channel_storage, SCL)
		# floats are not necessarily per bone, so don't check for membership in bones_lut
		floats_names = [name for name, channels in channel_storage.items() if FLO in channels]
		mani_info.float_count = len(floats_names)
		# mani_info.scl_bone_count_related = mani_info.scl_bone_count_repeat = 0

		# fill in the actual keys data
		bone_dtype = Ushort if mani_info.dtype.use_ushort else Ubyte
		mani_info.keys = ManiBlock(mani_info.context, mani_info, bone_dtype)
		k = mani_info.keys
		k.pos_bones_names[:] = pos_names
		k.ori_bones_names[:] = ori_names
		k.scl_bones_names[:] = scl_names
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


def fill_in_rest_data(m_name, mat_local_to_parent, rest_data):
	pos, quat, sca = mat_local_to_parent.decompose()
	rest_data[m_name] = {}
	rest_data[m_name][ORI] = [quat.x, quat.y, quat.z, quat.w]
	rest_data[m_name][POS] = pos
	rest_data[m_name][SCL] = sca


def sample_fcu(fcu, first_frame, last_frame, mani_info):
	keys = np.empty(mani_info.frame_count)
	keys[:] = [fcu.evaluate(i) for i in range(first_frame, last_frame)]
	return keys


def add_normed_float_keys(channel_storage, keys, needed_axes, float_name, game):
	# not used on JWE2
	if game in ("Jurassic World Evolution", "Planet Zoo"):
		# todo S is not completely correct in PZ, some misalignment remains apparently, needs to be scaled by about 1.1
		# S Motion Track ~ norm of X, Y, Z
		# T Motion Track ~ abs(RotY), probably also norm because usually only Y is used
		# make relative to first key
		# including all channels makes no difference
		val = np.array(keys[:, needed_axes])
		# val = np.array(keys)
		# val -= val[0]
		# calculate the length of the vector for each frame
		channel_storage[float_name] = {}
		res = np.linalg.norm(val, axis=1)
		res -= res[0]
		channel_storage[float_name][FLO] = res


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
