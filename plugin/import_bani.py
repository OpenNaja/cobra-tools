import os
import math

import bpy
import mathutils

from generated.formats.bani import BaniFile
from plugin.modules_export.armature import get_armature
from plugin.helpers import create_ob


def load_bani(file_path):
	"""Loads a bani from the given file path"""
	print("Importing {0}".format(file_path))

	data = BaniFile()
	# open file for binary reading
	data.load(file_path)
	return data


def create_anim(ob, anim_name):
	action = bpy.data.actions.new(name=anim_name)
	action.use_fake_user = True
	ob.animation_data_create()
	ob.animation_data.action = action
	return action


def load(files=[], filepath="", set_fps=False):
	dirname, filename = os.path.split(filepath)
	data = load_bani(filepath)
	data.read_banis()
	print(data)
	# data 0 has various scales and counts
	anim_length = data.data.animation_length
	num_frames = data.data.num_frames
	
	global_corr_euler = mathutils.Euler([math.radians(k) for k in (0, -90, -90)])
	global_corr_mat = global_corr_euler.to_matrix().to_4x4()
	
	fps = int(round(num_frames/anim_length))
	bpy.context.scene.frame_start = 0
	bpy.context.scene.frame_end = num_frames-1
	print("Banis fps", fps)
	ob = get_armature()

	bones_table = sorted([(bone["index"], bone.name) for bone in ob.pose.bones])
	bone_names = [tup[1] for tup in bones_table]

	# assert( len(bone_names) == len(data.bones_frames_eulers) == len(data.bones_frames_locs) )
	action = create_anim(ob, filename)
	# go over list of euler keys
	for i, bone_name in bones_table:
		empty = create_ob(bone_name, None)
		empty.scale = (0.01, 0.01, 0.01)
		for frame_i in range(data.data.num_frames):
			bpy.context.scene.frame_set(frame_i)
			euler = data.eulers[frame_i, i]
			loc = data.locs[frame_i, i]
			bpy.context.scene.frame_set(frame_i)
			empty.location = loc
			empty.keyframe_insert(data_path="location", frame=frame_i)

	for i, bone_name in bones_table:
		print(i, bone_name)
		# get pose pbone
		pbone = ob.pose.bones[bone_name]
		pbone.rotation_mode = "XYZ"
		# get object mode bone
		obone = ob.data.bones[bone_name]
		armature_space_matrix = obone.matrix_local
		data_type = "rotation_euler"
		# fcu = [action.fcurves.new(data_path=f'pose.bones["{bone_name}"].{data_type}', index=i, action_group=bone_name) for i in (0, 1, 2)]
		for frame_i in range(data.data.num_frames):
			bpy.context.scene.frame_set(frame_i)
			euler = data.eulers[frame_i, i]
			loc = data.locs[frame_i, i]
			euler = mathutils.Euler([math.radians(k) for k in euler])
			# experiments
			# trans = (global_corr_mat @ mathutils.Vector(loc)) + armature_space_matrix.translation

			# mdl2 vectors: (-x,-z,y)
			# loc = mathutils.Vector((-loc[0], -loc[2], loc[1]))
			loc = mathutils.Vector(loc)
			# trans = (mathutils.Vector(loc)) + armature_space_matrix.translation

			# the eulers are applied globally to the bone, equivalent to the user doing R+X, R+Y, R+Z for each axis.
			# this expresses the rotation that should be done in blender coordinates about the center of the bone
			space_corrected_rot = global_corr_mat @ euler.to_matrix().to_4x4()

			# rot_mat is the final armature space matrix of the posed bone
			rot_mat = space_corrected_rot @ armature_space_matrix

			# for fcurve, k in zip(fcu, e):
			# 	fcurve.keyframe_points.insert(frame_i, k)#.interpolation = "Linear"

			# rot_mat.translation = (space_corrected_rot @ loc) + armature_space_matrix.translation
			# loc_key = (space_corrected_rot @ mathutils.Vector(loc))
			loc_key = (euler.to_matrix().to_4x4() @ loc)
			# loc_key = ( loc @ space_corrected_rot)
			# loc_key = mathutils.Vector((-loc_key[0], -loc_key[2], loc_key[1]))
			# rot_mat.translation = loc_key + armature_space_matrix.translation
			# the ideal translation as calculated by blender
			rot_mat.translation = pbone.matrix.translation
			# print(rot_mat)
			pbone.matrix = rot_mat

			pbone.keyframe_insert(data_path="rotation_euler", frame=frame_i, group=bone_name)
			pbone.keyframe_insert(data_path="location", frame=frame_i, group=bone_name)
	return {'FINISHED'}
