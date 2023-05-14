import logging
import os
import time

import bpy
import mathutils

from generated.formats.manis import ManisFile
from plugin.export_manis import get_local_bone
from plugin.modules_export.armature import get_armature
from plugin.modules_import.anim import Animation
from plugin.utils.matrix_util import bone_name_for_blender
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
		logging.info(f"Importing '{b_name}'")
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
	corrector = ManisCorrector(False)
	scene = bpy.context.scene

	b_armature_ob = get_armature(scene)
	if not b_armature_ob:
		logging.warning(f"No armature was found in scene '{scene.name}' - did you delete it?")
	starttime = time.time()
	manis = ManisFile()
	manis.load(filepath)

	bones_data = {}
	for bone in b_armature_ob.data.bones:
		bones_data[bone.name] = get_local_bone(bone).inverted()

	for mi in manis.mani_infos:
		b_action = anim_sys.create_action(b_armature_ob, mi.name)
		if mi.dtype != 0:
			logging.info(f"{mi.name} is compressed, only uncompressed are imported")
			continue
		k = mi.keys
		for frame_i, key, bonerestmat_inv, fcurves in iter_keys(
				k.pos_bones, k.key_data.pos_bones, bones_data, b_action, "location"):
			key = mathutils.Vector([key.x, key.y, key.z])
			key = (bonerestmat_inv @ corrector.nif_bind_to_blender_bind(mathutils.Matrix.Translation(key))).to_translation()
			anim_sys.add_key(fcurves, frame_i, key, interp_loc)
		for frame_i, key, bonerestmat_inv, fcurves in iter_keys(
				k.ori_bones, k.key_data.ori_bones, bones_data, b_action, "rotation_quaternion"):
			# b_cam_ob.rotation_mode = "QUATERNION"
			key = mathutils.Quaternion([key.w, key.x, key.y, key.z])
			key = (bonerestmat_inv @ corrector.nif_bind_to_blender_bind(key.to_matrix().to_4x4())).to_quaternion()
			anim_sys.add_key(fcurves, frame_i, key, interp_loc)
		for frame_i, key, bonerestmat_inv, fcurves in iter_keys(
				k.scl_bones, k.key_data.scl_bones, bones_data, b_action, "scale"):
			key = mathutils.Vector([key.x, key.y, key.z])
			anim_sys.add_key(fcurves, frame_i, key, interp_loc)
		# only known for camera atm
		# b_cam_data = bpy.data.cameras.new("ManisCamera")
		# b_cam_ob = create_ob(scene, "Camera", b_cam_data)
		# b_data_action = anim_sys.create_action(b_cam_data, mi.name+"Data")
		# for float_name, keys in zip(k.floats, k.key_data.floats):
		# 	fcurves = anim_sys.create_fcurves(b_data_action, "lens", (0,))
		# 	# print(float_name, keys)
		# 	for frame, val in enumerate(keys):
		# 		anim_sys.add_key(fcurves, frame, (10 / val,), interp_loc)

	bpy.context.scene.frame_start = 0
	bpy.context.scene.frame_end = mi.frame_count
	bpy.context.scene.render.fps = int(round(mi.frame_count / mi.duration))
	return {'FINISHED'}
