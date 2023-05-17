import logging
import math
import os
import time

import bpy
import mathutils

from generated.formats.manis import ManisFile
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


def iter_keys(m_bone_names, m_keys, bones_data, b_action, b_dtype):
	for bone_i, m_name in enumerate(m_bone_names):
		b_name = bone_name_for_blender(m_name)
		logging.debug(f"Importing '{b_name}'")
		if b_name in bones_data:
			bonerestmat_inv = bones_data[b_name]
			b_channel = b_name
		else:
			bonerestmat_inv = mathutils.Matrix().to_4x4()
			b_channel = None
		fcurves = anim_sys.create_fcurves(b_action, b_dtype, dt_size[b_dtype], None, b_channel)
		for frame_i, frame in enumerate(m_keys):
			key = frame[bone_i]
			yield frame_i, key, bonerestmat_inv, fcurves


def load(files=[], filepath="", set_fps=False):
	starttime = time.time()
	corrector = ManisCorrector(False)
	scene = bpy.context.scene

	bones_data = {}
	b_armature_ob = get_armature(scene)
	if not b_armature_ob:
		logging.warning(f"No armature was found in scene '{scene.name}' - did you delete it?")
		b_cam_data = bpy.data.cameras.new("ManisCamera")
		b_armature_ob = create_ob(scene, "ManisCamera", b_cam_data)
		b_armature_ob.rotation_mode = "QUATERNION"
		cam_corr = mathutils.Euler((math.radians(90), 0, math.radians(-90))).to_quaternion()
	else:
		for bone in b_armature_ob.data.bones:
			bones_data[bone.name] = get_local_bone(bone).inverted()
		cam_corr = None
	manis = ManisFile()
	manis.load(filepath)

	for mi in manis.mani_infos:
		b_action = anim_sys.create_action(b_armature_ob, mi.name)
		if mi.dtype.compression != 0:
			logging.info(f"{mi.name} is compressed, only uncompressed are imported")
			b_action.use_frame_range = True
			b_action.frame_start = 0
			b_action.frame_end = mi.frame_count
			continue
		logging.info(f"Importing '{mi.name}'")
		k = mi.keys
		for frame_i, key, bonerestmat_inv, fcurves in iter_keys(
				k.pos_bones, k.key_data.pos_bones, bones_data, b_action, "location"):
			key = mathutils.Vector([key.x, key.y, key.z])
			# todo correct for scale
			key = (bonerestmat_inv @ corrector.nif_bind_to_blender_bind(mathutils.Matrix.Translation(key))).to_translation()
			anim_sys.add_key(fcurves, frame_i, key, interp_loc)
		for frame_i, key, bonerestmat_inv, fcurves in iter_keys(
				k.ori_bones, k.key_data.ori_bones, bones_data, b_action, "rotation_quaternion"):
			key = mathutils.Quaternion([key.w, key.x, key.y, key.z])
			key = (bonerestmat_inv @ corrector.nif_bind_to_blender_bind(key.to_matrix().to_4x4())).to_quaternion()
			if cam_corr is not None:
				out = mathutils.Quaternion(cam_corr)
				out.rotate(key)
				key = out
			anim_sys.add_key(fcurves, frame_i, key, interp_loc)
		for frame_i, key, bonerestmat_inv, fcurves in iter_keys(
				k.scl_bones, k.key_data.scl_bones, bones_data, b_action, "scale"):
			# swizzle
			key = mathutils.Vector([key.z, key.y, key.x])
			# correct axes
			mat = get_scale_mat(key)
			key = corrector.nif_bind_to_blender_bind(mat).to_scale()
			anim_sys.add_key(fcurves, frame_i, key, interp_loc)
		# these can vary in use according to the name of the channel
		for bone_i, m_name in enumerate(k.floats):
			b_name = bone_name_for_blender(m_name)
			logging.info(f"Importing '{b_name}'")
			# only known for camera
			if m_name == "CameraFOV":
				b_data_action = anim_sys.create_action(b_cam_data, f"{mi.name}Data")
				fcurves = anim_sys.create_fcurves(b_data_action, "lens", (0,))
				for frame_i, frame in enumerate(k.key_data.floats):
					key = frame[bone_i]
					anim_sys.add_key(fcurves, frame_i, (10 / key,), interp_loc)
			else:
				logging.warning(f"Don't know how to import floats for '{b_name}'")

	bpy.context.scene.frame_start = 0
	bpy.context.scene.frame_end = mi.frame_count
	bpy.context.scene.render.fps = int(round(mi.frame_count / mi.duration))
	return {'FINISHED'}
