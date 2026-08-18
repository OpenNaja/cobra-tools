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
from plugin.modules_export.animation import get_b_local_matrix
from plugin.modules_export.armature import get_armature
from plugin.modules_import.anim import Animation
from plugin.utils.anim import c_map
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
		# print(mi)
		logging.debug(f"Compression = {mi.dtype.compression}")
		k = mi.keys
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
				# correct for scale
				if scale_i is not None:
					scale = k.scl_bones[frame_i, scale_i]
					key = mathutils.Vector([key[0] * scale[2], key[1] * scale[1], key[2] * scale[0]])
				else:
					key = mathutils.Vector(key)
				key = (b_local_inv_mat @ corrector.to_blender(mathutils.Matrix.Translation(key))).to_translation()
				out_keys[frame_i] = key
		for b_channel, b_local_inv_mat, out_keys, in_keys in get_channel(
				k.ori_bones_names, k.ori_bones, b_local_inv_mats, b_action, "rotation_quaternion"):
			for frame_i, key in enumerate(in_keys):
				key = mathutils.Quaternion([key[3], key[0], key[1], key[2]])
				key = (b_local_inv_mat @ corrector.to_blender(key.to_matrix().to_4x4())).to_quaternion()
				if cam_corr is not None:
					out = mathutils.Quaternion(cam_corr)
					out.rotate(key)
					key = out
				out_keys[frame_i] = key
		for b_channel, b_local_inv_mat, out_keys, in_keys in get_channel(
				k.scl_bones_names, k.scl_bones, b_local_inv_mats, b_action, "scale"):
			for frame_i, key in enumerate(in_keys):
				# swizzle
				key = mathutils.Vector([key[2], key[1], key[0]])
				# correct axes
				mat = get_scale_mat(key)
				key = corrector.to_blender(mat).to_scale()
				out_keys[frame_i] = key

	scene.frame_start = 0
	scene.frame_end = mi.frame_count-1
	scene.render.fps = int(round((mi.frame_count-1) / mi.duration))
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
