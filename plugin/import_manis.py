import logging
import math
import os
import time

import bpy
import mathutils
import numpy as np

from generated.formats.manis import ManisFile
from generated.formats.manis.versions import is_ztuac, is_dla
from generated.formats.wsm.structs.WsmHeader import WsmHeader
from plugin.modules_export.armature import get_armature
from plugin.modules_import.anim import Animation
from generated.formats.manis.acl import decode_file as decode_acl_file, normalize_frame_count
from plugin.utils.anim import c_map, get_b_local_matrix
from plugin.utils.blender_util import bone_name_for_blender, get_scale_mat
from plugin.utils.object import create_ob
from plugin.utils.transforms import ManisCorrector

interp_loc = None
anim_sys = Animation()
dt_size = {
	"location": tuple(range(3)),
	"rotation_quaternion": tuple(range(4)),
	"scale": tuple(range(3)),
}


def keep_quat_hemisphere(key, out_keys, frame_i):
	"""Keep a quaternion in the same hemisphere as the previous key.

	ACL stores rotations with w dropped and rebuilt as always-positive, so a
	rotation that crosses w=0 comes back as its antipode. q and -q are the same
	orientation, but blender interpolates between them the long way round, which
	spins the bone. Observed on mutadon head and jaw (9-11 flips per clip, dot
	exactly -1.0); indoraptor happened not to cross w=0, which is why it looked fine.
	"""
	if frame_i and float(np.dot(out_keys[frame_i - 1], (key.w, key.x, key.y, key.z))) < 0.0:
		return mathutils.Quaternion((-key.w, -key.x, -key.y, -key.z))
	return key


def key_unanimated_channels(b_ob, action):
	"""Give every bone a rest-value key on channels this action does not animate.

	In game a clip is applied to a fresh bind pose, so a channel the clip omits
	means "stay at bind". Blender instead leaves whatever the previously played
	action put there, so switching between clips that animate different channel
	sets drags stale offsets along. Observed on deinosuchus: standidle01 has no
	location channel for def_c_jawSquash_joint or def_frontLegLwrHalfTwist_joint.L,
	so both kept a 1.128 unit offset from an earlier clip - a tucked chin and a leg
	bone flung out to the side.

	One rest-value key per missing channel makes each action self-contained.
	"""
	rest = {
		"location": (0.0, 0.0, 0.0),
		"rotation_quaternion": (1.0, 0.0, 0.0, 0.0),
		"scale": (1.0, 1.0, 1.0),
	}
	keyed = {}
	for fcu in action.fcurves:
		if '"' not in fcu.data_path:
			continue
		bone_name = fcu.data_path.split('"')[1]
		channel = fcu.data_path.rsplit(".", 1)[-1]
		keyed.setdefault(bone_name, set()).add(channel)
	frame = int(action.frame_range[0])
	for p_bone in b_ob.pose.bones:
		have = keyed.get(p_bone.name, set())
		for channel, values in rest.items():
			if channel in have:
				continue
			data_path = f'pose.bones["{p_bone.name}"].{channel}'
			for i, value in enumerate(values):
				try:
					fcu = action.fcurves.new(data_path, index=i, action_group=p_bone.name)
				except RuntimeError:
					# already exists for this index, nothing to pad
					continue
				fcu.keyframe_points.insert(frame, value)


def get_channel(m_bone_names, m_keys, b_local_inv_mats, b_action, b_dtype):
	frames = range(len(m_keys))
	for bone_i, g_name in enumerate(m_bone_names):
		b_name = bone_name_for_blender(g_name)
		if b_name in b_local_inv_mats:
			b_local_inv_mat = b_local_inv_mats[b_name]
			b_channel = b_name
		else:
			# not sure if this is desired like that
			if g_name == "camera_joint":
				logging.debug(f"Object transform '{b_name}' as LocRotScale")
				b_local_inv_mat = mathutils.Matrix().to_4x4()
				b_channel = None
			else:
				logging.warning(f"Ignoring extraneous bone '{b_name}'")
				continue
		yield from keys_adder(b_action, b_channel, b_dtype, m_keys[:, bone_i], b_local_inv_mat, frames)


def keys_adder(b_action, b_channel, b_dtype, in_keys, b_local_inv_mat, frames):
	dt_range = dt_size[b_dtype]
	out_keys = np.empty((len(in_keys), len(dt_range)), float)
	yield b_channel, b_local_inv_mat, out_keys, in_keys
	anim_sys.add_keys(b_action, b_dtype, dt_range, None, frames, out_keys, None, n_bone=b_channel)


def import_wsm(corrector, b_action, folder, mani_info, bone_name, b_local_inv_mats):
	wsm_name = f"{mani_info.name}_{bone_name}.wsm"
	wsm_path = os.path.join(folder, wsm_name)
	if os.path.isfile(wsm_path):
		logging.info(f"Importing {wsm_name}")
		wsm = WsmHeader.from_xml_file(wsm_path, mani_info.context)
		b_local_inv_mat = b_local_inv_mats[bone_name]
		frames = range(wsm.frame_count)
		for b_channel, b_local_inv_mat, out_keys, in_keys in keys_adder(
				b_action, bone_name, "location", wsm.locs.data, b_local_inv_mat, frames):
			for frame_i, key in enumerate(in_keys):
				key = mathutils.Vector(key)
				key = (b_local_inv_mat @ corrector.to_blender(mathutils.Matrix.Translation(key))).to_translation()
				out_keys[frame_i] = key
		for b_channel, b_local_inv_mat, out_keys, in_keys in keys_adder(
				b_action, bone_name, "rotation_quaternion", wsm.quats.data, b_local_inv_mat, frames):
			for frame_i, key in enumerate(in_keys):
				key = mathutils.Quaternion([key.w, key.x, key.y, key.z])
				key = (b_local_inv_mat @ corrector.to_blender(key.to_matrix().to_4x4())).to_quaternion()
				out_keys[frame_i] = key


def load(reporter, files=(), filepath="", disable_ik=False, set_fps=False):
	try:
		import bitarray
		import bitarray.util
	except:
		reporter.show_error(f"Install the 'bitarray' module to blender to import compressed animations.\nRefer to the Cobra Tools wiki for help")

	start_time = time.time()
	folder, manis_name = os.path.split(filepath)
	scene = bpy.context.scene
	manis = ManisFile()
	manis.load(filepath)
	is_acl_manis = manis.context.version == 262 and manis.context.mani_version == 282
	acl_streams = iter(decode_acl_file(filepath)) if (
		is_acl_manis and any(mi.dtype.compression for mi in manis.mani_infos)
	) else iter(())
	# note that ZTUAC and PC share v257, however PC uses new transforms
	is_old_orientation = any((is_ztuac(manis.context), is_dla(manis.context)))
	if is_old_orientation and scene.cobra.game == "Planet Coaster":
		is_old_orientation = False
	corrector = ManisCorrector(is_old_orientation)

	b_local_inv_mats = {}
	b_armature_ob = get_armature(scene.objects)
	if not b_armature_ob:
		logging.warning(f"No armature was found in scene '{scene.name}' - did you delete it?")
	else:
		for p_bone in b_armature_ob.pose.bones:
			p_bone.rotation_mode = "QUATERNION"
			if disable_ik:
				for constraint in p_bone.constraints:
					if constraint.type == "IK":
						constraint.enabled = False
		for bone in b_armature_ob.data.bones:
			b_local_inv_mats[bone.name] = get_b_local_matrix(bone).inverted()
	cam_corr = None

	for mi in manis.mani_infos:
		logging.info(f"Importing {mi.name}")
		if "_camera" in mi.name:
			b_cam_data = bpy.data.cameras.new(mi.name)
			# b_cam_data.lens_unit = "FOV"  # no use, as blender can't animate FOV directly
			b_cam_data.sensor_width = 64  # eyeballed to match game
			b_armature_ob = create_ob(scene, mi.name, b_cam_data)
			b_armature_ob.rotation_mode = "QUATERNION"
			cam_corr = mathutils.Euler((math.radians(90), 0, math.radians(-90))).to_quaternion()
		b_action = anim_sys.create_action(b_armature_ob, mi.name)
		# store ovs name
		b_action["stream"] = manis.stream
		b_action["fps"] = int(round((mi.frame_count-1) / mi.duration))
		# print(mi)
		logging.debug(f"Compression = {mi.dtype.compression}")
		k = mi.keys
		use_acl = bool(is_acl_manis and mi.dtype.compression)
		if use_acl:
			# ACL is decoded by our external decoder rather than manis.decompress, but the
			# result lands in the same place: clear the compression flags and fill the
			# uncompressed key arrays, so the shared import path below serves both.
			transform_stream = next(acl_streams)
			if transform_stream.track_type != 12:
				raise ValueError(f"Expected ACL transform tracks for {mi.name}")
			if transform_stream.track_count != mi.target_bone_count:
				raise ValueError(
					f"ACL track count mismatch for {mi.name}: "
					f"{transform_stream.track_count} != {mi.target_bone_count}"
				)
			transforms = normalize_frame_count(transform_stream.values, mi.frame_count)
			if mi.float_count:
				scalar_stream = next(acl_streams)
				if scalar_stream.track_type != 0:
					raise ValueError(f"Expected ACL float1 tracks for {mi.name}")
				if scalar_stream.track_count != mi.float_count:
					raise ValueError(
						f"ACL scalar count mismatch for {mi.name}: "
						f"{scalar_stream.track_count} != {mi.float_count}"
					)
				k.floats = normalize_frame_count(scalar_stream.values[:, :, 0], mi.frame_count)
			mi.dtype.compression = 0
			mi.dtype.has_list = 0
			k.reset_field("pos_bones")
			k.reset_field("ori_bones")
			k.ori_bones[:] = transforms[:, np.asarray(k.ori_channel_to_bone), 0:4]
			k.pos_bones[:] = transforms[:, np.asarray(k.pos_channel_to_bone), 4:7]
		import_wsm(corrector, b_action, folder, mi, "srb", b_local_inv_mats)
		# floats are present for compressed or uncompressed
		# they can vary in use according to the name of the channel
		for bone_i, g_name in enumerate(k.floats_names):
			if "." in g_name:
				g_name, suffix = g_name.rsplit(".", 1)
			else:
				suffix = ""
			b_name = bone_name_for_blender(g_name)
			# logging.debug(f"Importing {b_name}")
			keys = k.floats[:, bone_i]
			samples = range(len(keys))
			if g_name == "CameraFOV":
				# focal_len = w /  tan(FOV / 2) / 2
				b_data_action = anim_sys.create_action(b_cam_data, f"{mi.name}_Data")
				# original sensor width
				keys = 36 / np.tan(keys / 2) / 2
				anim_sys.add_keys(b_data_action, "lens", (0,), None, samples, keys, None)
			elif b_name in b_local_inv_mats and suffix:
				# represented by animated properties of bone constraints
				p_bone = b_armature_ob.pose.bones[b_name]
				for c_suffix, c_type, create, limits in c_map:
					if suffix == c_suffix:
						if limits:
							l_min, l_max = limits
							keys -= l_min
							keys /= (l_max - l_min)
						b_constraint = get_constraint(p_bone, c_type, create=create)
						if b_constraint:
							anim_sys.add_keys(b_action, "influence", (0,), None, samples, keys, None, n_bone=b_name, n_constraint=b_constraint.name)
						break
				else:
					logging.warning(f"Don't know how to import '{suffix}' for '{b_name}'")
			elif "Motion Track" in g_name:
				logging.debug(f"Ignoring redundant import of '{g_name}'")
			else:
				logging.warning(f"Don't know how to import floats for '{b_name}'")
				# logging.debug(k.floats[:, bone_i])
		# check compression flag
		if mi.dtype.compression != 0:
			try:
				manis.decompress(mi)
			except:
				b_action.use_frame_range = True
				b_action.frame_start = 0
				b_action.frame_end = mi.frame_count-1
				reporter.show_error(f"Decompressing {mi.name} failed, skipping")
				continue

		scale_lut = {name: i for i, name in enumerate(k.scl_bones_names)}
		for b_channel, b_local_inv_mat, out_keys, in_keys in get_channel(
				k.pos_bones_names, k.pos_bones, b_local_inv_mats, b_action, "location"):
			scale_i = scale_lut.get(b_channel, None)
			for frame_i, key in enumerate(in_keys):
				# an all-NaN key marks a sub-track ACL stripped as equal to the bind pose
				if np.isnan(key).all():
					key = corrector.from_blender(b_local_inv_mat.inverted()).to_translation()
				# correct for scale - ACL clips carry no separate scale correction
				elif scale_i is not None and not use_acl:
					scale = k.scl_bones[frame_i, scale_i]
					key = mathutils.Vector([key[0] * scale[2], key[1] * scale[1], key[2] * scale[0]])
				else:
					key = mathutils.Vector(key)
				key = (b_local_inv_mat @ corrector.to_blender(mathutils.Matrix.Translation(key))).to_translation()
				out_keys[frame_i] = key
		for b_channel, b_local_inv_mat, out_keys, in_keys in get_channel(
				k.ori_bones_names, k.ori_bones, b_local_inv_mats, b_action, "rotation_quaternion"):
			for frame_i, key in enumerate(in_keys):
				# an all-NaN key marks a sub-track ACL stripped as equal to the bind pose
				if np.isnan(key).all():
					g_key = corrector.from_blender(b_local_inv_mat.inverted()).to_quaternion()
				else:
					g_key = mathutils.Quaternion([key[3], key[0], key[1], key[2]])
				b_key = (b_local_inv_mat @ corrector.to_blender(g_key.to_matrix().to_4x4())).to_quaternion()
				if cam_corr is not None:
					out = mathutils.Quaternion(cam_corr)
					out.rotate(b_key)
					b_key = out
				out_keys[frame_i] = keep_quat_hemisphere(b_key, out_keys, frame_i)
		for b_channel, b_local_inv_mat, out_keys, in_keys in get_channel(
				k.scl_bones_names, k.scl_bones, b_local_inv_mats, b_action, "scale"):
			for frame_i, key in enumerate(in_keys):
				# swizzle
				key = mathutils.Vector([key[2], key[1], key[0]])
				# correct axes
				mat = get_scale_mat(key)
				key = corrector.to_blender(mat).to_scale()
				out_keys[frame_i] = key
		key_unanimated_channels(b_armature_ob, b_action)

	reporter.show_info(f"Imported {manis_name}in {time.time()-start_time:.2f} s")


def get_constraint(p_bone, c_type="IK", create=True):
	for const in p_bone.constraints:
		if const.type == c_type:
			return const
	if not create:
		logging.warning(f"Trying to animate '{c_type}' property on bone '{p_bone.name}' without IK constraint")
		return None
	else:
		const = p_bone.constraints.new(c_type)
		return const
