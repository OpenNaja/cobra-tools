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


def load(files=[], filepath="", set_fps=False):
	corrector = ManisCorrector(False)
	scene = bpy.context.scene

	b_armature_ob = get_armature(scene)
	if not b_armature_ob:
		logging.warning(f"No armature was found in scene '{scene.name}' - did you delete it?")
	anim_sys = Animation()
	starttime = time.time()
	manis = ManisFile()
	manis.load(filepath)

	bones_data = {}
	for bone in b_armature_ob.data.bones:
		bones_data[bone.name] = get_local_bone(bone).inverted()

	for mi in manis.mani_infos:
		assert mi.dtype == 0, "Only uncompressed is supported"
		b_action = anim_sys.create_action(b_armature_ob, mi.name)
		k = mi.keys
		for bone_i, pos_bone in enumerate(k.pos_bones):
			b_name = bone_name_for_blender(pos_bone)
			logging.info(f"Importing loc '{b_name}'")
			bonerestmat_inv = bones_data[b_name]
			fcurves = anim_sys.create_fcurves(b_action, "location", range(3), None, b_name)
			for frame_i, frame in enumerate(k.key_data.pos_bones):
				key = frame[bone_i]
				key = mathutils.Vector([key.x, key.y, key.z])
				key = (bonerestmat_inv @ corrector.nif_bind_to_blender_bind(mathutils.Matrix.Translation(key))).to_translation()
				anim_sys.add_key(fcurves, frame_i, key, interp_loc)
		for bone_i, ori_bone in enumerate(k.ori_bones):
			b_name = bone_name_for_blender(ori_bone)
			logging.info(f"Importing rot '{b_name}'")
			bonerestmat_inv = bones_data[b_name]
			# b_cam_ob.rotation_mode = "QUATERNION"
			fcurves = anim_sys.create_fcurves(b_action, "rotation_quaternion", range(4), None, b_name)
			for frame_i, frame in enumerate(k.key_data.ori_bones):
				key = frame[bone_i]
				key = mathutils.Quaternion([key.w, key.x, key.y, key.z])
				key = (bonerestmat_inv @ corrector.nif_bind_to_blender_bind(key.to_matrix().to_4x4())).to_quaternion()
				anim_sys.add_key(fcurves, frame_i, key, interp_loc)
		# only known for camera atm
		# b_cam_data = bpy.data.cameras.new("TestCamera")
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
