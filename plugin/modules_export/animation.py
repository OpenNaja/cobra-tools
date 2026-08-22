import logging

import bpy
import mathutils
import numpy as np

from generated.formats.manis import POS, ORI, srb_name, EUL, SCL
from plugin.utils.blender_util import bone_name_for_ovl, get_scale_mat


def store_pose_frame_info(b_ob, src_frame, trg_frame, b_local_mats, channel_storage, corrector, cam_corr):
	bpy.context.scene.frame_set(src_frame)
	bpy.context.view_layer.update()
	if b_ob.type == "CAMERA":
		store_transform_data(channel_storage, corrector, b_ob.matrix_local, "camera_joint", src_frame, trg_frame, cam_corr)
	elif b_ob.type == "ARMATURE":
		for b_name, p_bone in b_ob.pose.bones.items():
			g_name = bone_name_for_ovl(b_name)
			# Get the final transform of the bone in its own local space...
			# then make it relative to the parent bone
			# transform is stored relative to the parent rest
			# whereas blender stores translation relative to the bone itself, not the parent
			b_local_posed_matrix = b_local_mats[g_name] @ b_ob.convert_space(
				pose_bone=p_bone, matrix=p_bone.matrix, from_space='POSE', to_space='LOCAL')
			store_transform_data(channel_storage, corrector, b_local_posed_matrix, g_name, src_frame, trg_frame, cam_corr)


def store_transform_data(channel_storage, corrector, b_local_posed_matrix, g_name, src_frame, trg_frame, cam_corr):
	# loc
	v = sample_scale2(b_local_posed_matrix, src_frame, inverted=True) @ b_local_posed_matrix
	channel_storage[g_name][POS][trg_frame] = corrector.from_blender(v).to_translation()
	# rot
	final_m = corrector.from_blender(b_local_posed_matrix)
	key = final_m.to_quaternion()
	if cam_corr is not None:
		out = mathutils.Quaternion(cam_corr)
		key.rotate(out)
		key = mathutils.Quaternion((key.x, -key.y, key.w, -key.z))
	# swizzle - w is stored last
	channel_storage[g_name][ORI][trg_frame] = key.x, key.y, key.z, key.w
	if g_name == srb_name:
		channel_storage[g_name][EUL][trg_frame] = key.to_euler()
	# scale
	scale_mat = sample_scale2(b_local_posed_matrix, src_frame)
	# needs axis correction, but appears to be stored relative to the animated bone's axes
	scale_mat = corrector.from_blender(scale_mat)
	# swizzle
	key = scale_mat.to_scale()
	channel_storage[g_name][SCL][trg_frame] = key.z, key.y, key.x


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


def fill_in_rest_data(g_name, g_local_matrix, g_rest_data):
	pos, quat, sca = g_local_matrix.decompose()
	g_rest_data[g_name] = {}
	g_rest_data[g_name][ORI] = [quat.x, quat.y, quat.z, quat.w]
	g_rest_data[g_name][POS] = pos
	g_rest_data[g_name][SCL] = sca


def sample_fcu(fcu, first_frame, last_frame, mani_info):
	keys = np.empty(mani_info.frame_count)
	keys[:] = [fcu.evaluate(i) for i in range(first_frame, last_frame)]
	return keys


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
