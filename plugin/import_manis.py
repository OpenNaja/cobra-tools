import contextlib
import logging
import math
import os
import time

import bpy
import mathutils

from generated.formats.manis import ManisFile
from generated.formats.wsm.compounds.WsmHeader import WsmHeader
from plugin.export_manis import get_local_bone
from plugin.modules_export.armature import get_armature
from plugin.modules_import.anim import Animation
from plugin.utils.matrix_util import bone_name_for_blender, get_scale_mat
from plugin.utils.object import create_ob
from plugin.utils.transforms import ManisCorrector

interp_loc = None
anim_sys = Animation()
dt_size = {
	"location": tuple(range(3)),
	"rotation_quaternion": tuple(range(4)),
	"scale": tuple(range(3)),
}


def get_channel(m_bone_names, m_keys, bones_data, b_action, b_dtype):
	for bone_i, m_name in enumerate(m_bone_names):
		b_name = bone_name_for_blender(m_name)
		logging.debug(f"Importing '{b_name}'")
		if b_name in bones_data:
			bonerestmat_inv = bones_data[b_name]
			b_channel = b_name
		else:
			# not sure this is desired like that
			if bones_data:
				logging.warning(f"Ignoring extraneous bone '{b_name}'")
				continue
			else:
				logging.debug(f"Object transform '{b_name}' as LocRotScale")
				bonerestmat_inv = mathutils.Matrix().to_4x4()
				b_channel = None
		yield from keys_adder(b_action, b_channel, b_dtype, m_keys[:, bone_i], bonerestmat_inv)


def keys_adder(b_action, b_channel, b_dtype, in_keys, bonerestmat_inv):
	out_keys = []
	out_frames = []
	yield b_channel, bonerestmat_inv, out_frames, out_keys, in_keys
	anim_sys.add_keys(b_action, b_dtype, dt_size[b_dtype], None, out_frames, out_keys, None, bone_name=b_channel)


def import_wsm(corrector, b_action, folder, mani_info, bone_name, bones_data):
	wsm_name = f"{mani_info.name}_{bone_name}.wsm"
	wsm_path = os.path.join(folder, wsm_name)
	if os.path.isfile(wsm_path):
		logging.info(f"Importing {wsm_name}")
		wsm = WsmHeader.from_xml_file(wsm_path, mani_info.context)
		# print(wsm)
		bonerestmat_inv = bones_data[bone_name]
		for b_channel, bonerestmat_inv, out_frames, out_keys, in_keys in keys_adder(
				b_action, bone_name, "location", wsm.locs.data, bonerestmat_inv):
			for frame_i, key in enumerate(in_keys):
				key = mathutils.Vector(key)
				key = (bonerestmat_inv @ corrector.to_blender(mathutils.Matrix.Translation(key))).to_translation()
				out_frames.append(frame_i)
				out_keys.append(key)
		for b_channel, bonerestmat_inv, out_frames, out_keys, in_keys in keys_adder(
				b_action, bone_name, "rotation_quaternion", wsm.quats.data, bonerestmat_inv):
			for frame_i, key in enumerate(in_keys):
				key = mathutils.Quaternion([key.w, key.x, key.y, key.z])
				key = (bonerestmat_inv @ corrector.to_blender(key.to_matrix().to_4x4())).to_quaternion()
				out_frames.append(frame_i)
				out_keys.append(key)


def stash(b_ob, action, track_name, start_frame):
	# Simulate stash :
	# * add a track
	# * add an action on track
	# * lock & mute the track
	# * remove active action from object
	tracks = b_ob.animation_data.nla_tracks
	new_track = tracks.new(prev=None)
	new_track.name = track_name
	strip = new_track.strips.new(action.name, start_frame, action)
	new_track.lock = True
	new_track.mute = True
	# nah
	# b_ob.animation_data.action = None


def load(reporter, files=(), filepath="", set_fps=False):
	folder, manis_name = os.path.split(filepath)
	starttime = time.time()
	corrector = ManisCorrector(False)
	scene = bpy.context.scene

	bones_data = {}
	b_armature_ob = get_armature(scene.objects)
	if not b_armature_ob:
		logging.warning(f"No armature was found in scene '{scene.name}' - did you delete it?")
		b_cam_data = bpy.data.cameras.new("ManisCamera")
		b_armature_ob = create_ob(scene, "ManisCamera", b_cam_data)
		b_armature_ob.rotation_mode = "QUATERNION"
		cam_corr = mathutils.Euler((math.radians(90), 0, math.radians(-90))).to_quaternion()
	else:
		for p_bone in b_armature_ob.pose.bones:
			p_bone.rotation_mode = "QUATERNION"
		for bone in b_armature_ob.data.bones:
			bones_data[bone.name] = get_local_bone(bone).inverted()
		cam_corr = None
	manis = ManisFile()
	manis.load(filepath)

	for mi in manis.mani_infos:
		b_action = anim_sys.create_action(b_armature_ob, mi.name)
		stash(b_armature_ob, b_action, mi.name, 0)
		print(mi)
		k = mi.keys
		import_wsm(corrector, b_action, folder, mi, "srb", bones_data)
		# floats are present for compressed or uncompressed
		# they can vary in use according to the name of the channel
		for bone_i, m_name in enumerate(k.floats_names):
			b_name = bone_name_for_blender(m_name)
			logging.info(f"Importing '{b_name}'")
			# only known for camera
			if m_name == "CameraFOV":
				b_data_action = anim_sys.create_action(b_cam_data, f"{mi.name}Data")
				fcurves = anim_sys.create_fcurves(b_data_action, "lens", (0,))
				for frame_i, frame in enumerate(k.floats):
					key = frame[bone_i]
					anim_sys.add_key(fcurves, frame_i, (10 / key,), interp_loc)
			else:
				logging.warning(f"Don't know how to import floats for '{b_name}'")
				logging.debug(k.floats[:, bone_i])
		# check compression flag
		if mi.dtype.compression != 0:
			logging.info(f"{mi.name} is compressed, trying to import anyway")
			ck = k.compressed
			try:
				manis.decompress(None, mi)
			except:
				b_action.use_frame_range = True
				b_action.frame_start = 0
				b_action.frame_end = mi.frame_count-1
				logging.exception(f"Decompressing {mi.name} failed, skipping")
				continue

			for b_channel, bonerestmat_inv, out_frames, out_keys, in_keys in get_channel(
					k.pos_bones_names, ck.pos_bones, bones_data, b_action, "location"):
				for frame_i, key in enumerate(in_keys):
					key = mathutils.Vector(key)
					# # correct for scale
					# if scale:
					# 	key = mathutils.Vector([key.x * scale.z, key.y * scale.y, key.z * scale.x])
					key = (bonerestmat_inv @ corrector.to_blender(mathutils.Matrix.Translation(key))).to_translation()
					out_frames.append(frame_i)
					out_keys.append(key)
			for b_channel, bonerestmat_inv, out_frames, out_keys, in_keys in get_channel(
				k.ori_bones_names, ck.ori_bones, bones_data, b_action, "rotation_quaternion"):
				for frame_i, key in enumerate(in_keys):
					# if frame_i % 32:
					# 	continue
					key = mathutils.Quaternion([key[3], key[0], key[1], key[2]])
					# if frame_i == 0 and b_name == "def_c_hips_joint":
					# 	logging.info(f"{mi.name} {key}")
					key = (bonerestmat_inv @ corrector.to_blender(key.to_matrix().to_4x4())).to_quaternion()
					# if cam_corr is not None:
					# 	out = mathutils.Quaternion(cam_corr)
					# 	out.rotate(key)
					# 	key = out
					out_frames.append(frame_i)
					out_keys.append(key)
			# skip uncompressed anim
			continue
		logging.info(f"Importing '{mi.name}'")
		scale_lut = {name: i for i, name in enumerate(k.scl_bones_names)}
		for b_channel, bonerestmat_inv, out_frames, out_keys, in_keys in get_channel(
				k.pos_bones_names, k.pos_bones, bones_data, b_action, "location"):
			scale_i = scale_lut.get(b_channel, None)
			for frame_i, key in enumerate(in_keys):
				# correct for scale
				if scale_i is not None:
					scale = k.scl_bones[frame_i, scale_i]
					key = mathutils.Vector([key[0] * scale[2], key[1] * scale[1], key[2] * scale[0]])
				else:
					key = mathutils.Vector(key)
				key = (bonerestmat_inv @ corrector.to_blender(mathutils.Matrix.Translation(key))).to_translation()
				out_frames.append(frame_i)
				out_keys.append(key)
		for b_channel, bonerestmat_inv, out_frames, out_keys, in_keys in get_channel(
				k.ori_bones_names, k.ori_bones, bones_data, b_action, "rotation_quaternion"):
			for frame_i, key in enumerate(in_keys):
				key = mathutils.Quaternion([key[3], key[0], key[1], key[2]])
				key = (bonerestmat_inv @ corrector.to_blender(key.to_matrix().to_4x4())).to_quaternion()
				if cam_corr is not None:
					out = mathutils.Quaternion(cam_corr)
					out.rotate(key)
					key = out
				out_frames.append(frame_i)
				out_keys.append(key)
		for b_channel, bonerestmat_inv, out_frames, out_keys, in_keys in get_channel(
				k.scl_bones_names, k.scl_bones, bones_data, b_action, "scale"):
			for frame_i, key in enumerate(in_keys):
				# swizzle
				key = mathutils.Vector([key[2], key[1], key[0]])
				# correct axes
				mat = get_scale_mat(key)
				key = corrector.to_blender(mat).to_scale()
				out_frames.append(frame_i)
				out_keys.append(key)

	scene.frame_start = 0
	scene.frame_end = mi.frame_count-1
	scene.render.fps = int(round((mi.frame_count-1) / mi.duration))
	reporter.show_info(f"Imported {manis_name}")
