import os
import time

import bpy
import mathutils
from bpy_extras.io_utils import axis_conversion

from generated.formats.manis import ManisFile
from plugin.modules_import.anim import Animation
from plugin.utils.object import create_ob
from plugin.utils.transforms import ManisCorrector

interp_loc = None


def load(files=[], filepath="", set_fps=False):
	# global_corr_euler = mathutils.Euler([math.radians(k) for k in (0, 0, 0)])
	corrector = ManisCorrector(False)
	# axis_conversion(from_forward='Y', from_up='Z', to_forward='Y', to_up='Z')
	global_corr_mat = axis_conversion("Z", "Y").to_4x4()
	# global_corr_mat = corrector.correction_glob
	# n_bind = mathutils.Matrix(joint_transform.rot.data).inverted().to_4x4()
	# n_bind.translation = (joint_transform.loc.x, joint_transform.loc.y, joint_transform.loc.z)
	# b_bind = corrector.nif_bind_to_blender_bind(n_bind)
	anim_sys = Animation()
	starttime = time.time()
	dirname, filename = os.path.split(filepath)
	# basename, ext = os.path.splitext(filename)
	data = ManisFile()
	# open file for binary reading
	data.load(filepath)
	# print(data)
	scene = bpy.context.scene
	b_cam_data = bpy.data.cameras.new("TestCamera")
	b_cam_ob = create_ob(scene, "Camera", b_cam_data)
	for mi in data.mani_infos:
		assert mi.b == 0, "Only uncompressed is supported"
		b_action = anim_sys.create_action(b_cam_ob, mi.name)
		mb = mi.keys
		for pos_bone, keys in zip(mb.pos_bones, mb.key_data.pos_bones):
			fcurves = anim_sys.create_fcurves(b_action, "location", range(3))
			# print(pos_bone, keys)
			for frame, val in enumerate(keys):
				key = mathutils.Vector([val.x, val.y, val.z])
				key = corrector.nif_bind_to_blender_bind(mathutils.Matrix.Translation(key)).to_translation()
				# key = (global_corr_mat @ mathutils.Matrix.Translation(key)).to_translation()
				anim_sys.add_key(fcurves, frame, key, interp_loc)
		for ori_bone, keys in zip(mb.ori_bones, mb.key_data.ori_bones):
			b_cam_ob.rotation_mode = "QUATERNION"
			fcurves = anim_sys.create_fcurves(b_action, "rotation_quaternion", range(4))
			# print(ori_bone, keys)
			for frame, val in enumerate(keys):
				key = mathutils.Quaternion([val.w, val.x, val.y, val.z])
				key = corrector.nif_bind_to_blender_bind(key.to_matrix().to_4x4()).to_quaternion()
				# key = (global_corr_mat @ key.to_matrix().to_4x4()).to_quaternion()
				# do a 180° flip, probably unique to camera as faces in the wrong direction even without any correction
				key = (-key.w, key.x, key.y, -key.z)
				anim_sys.add_key(fcurves, frame, key, interp_loc)
		b_data_action = anim_sys.create_action(b_cam_data, mi.name+"Data")
		for float_name, keys in zip(mb.floats, mb.key_data.floats):
			fcurves = anim_sys.create_fcurves(b_data_action, "lens", (0,))
			# print(float_name, keys)
			for frame, val in enumerate(keys):
				anim_sys.add_key(fcurves, frame, (10 / val,), interp_loc)

	bpy.context.scene.frame_start = 0
	bpy.context.scene.frame_end = mi.frame_count
	bpy.context.scene.render.fps = int(round(mi.frame_count / mi.duration))
	return {'FINISHED'}
