import logging
import os
import math

import bpy
import mathutils

from generated.formats.bani import BanisFile
from plugin.modules_export.armature import get_armature
from plugin.modules_import.anim import create_anim, Animation
from plugin.utils.matrix_util import Corrector
from plugin.utils.object import create_ob


def load_banis(file_path):
	"""Loads a bani from the given file path"""
	print(f"Importing {file_path}")

	data = BanisFile()
	# open file for binary reading
	data.load(file_path)
	return data


interp_loc = None
# global_corr_euler = mathutils.Euler([math.radians(k) for k in (0, -90, -90)])
global_corr_euler = mathutils.Euler([math.radians(k) for k in (0, 0, 0)])
# global_corr_euler = mathutils.Euler([math.radians(k) for k in (90, 90, 90)])
global_corr_mat = global_corr_euler.to_matrix().to_4x4()


def load(files=[], filepath="", set_fps=False):
	scene = bpy.context.scene
	b_armature_ob = get_armature(scene)

	p_bones = sorted(b_armature_ob.pose.bones, key=lambda pbone: pbone["index"])
	bones_table = [(bone["index"], bone.name) for bone in p_bones]
	bone_names = [tup[1] for tup in bones_table]
	anim_sys = Animation()
	banis = load_banis(filepath)
	print(banis)
	for bani in banis.anims:
		# data 0 has various scales and counts
		anim_length = bani.data.animation_length
		num_frames = bani.data.num_frames

		scene.frame_start = 0
		scene.frame_end = num_frames-1
		fps = int(round(num_frames/anim_length))
		# print(f"Banis fps = {fps}")
		animate_empties(anim_sys, bones_table, bani, scene, b_armature_ob)

	# go over list of euler keys
	for i, bone_name in bones_table:
		b_empty_ob = create_ob(scene, f"rest_{bone_name}", None)
		bind = b_armature_ob.data.bones[bone_name].matrix_local
		# bind = corrector.blender_bind_to_nif_bind(bind)
		# b_empty_ob.matrix_local = bind.inverted()
		# b_empty_ob.matrix_local = bind.inverted()
		b_empty_ob.location = bind.translation
		b_empty_ob.scale = (0.01, 0.01, 0.01)
	return {'FINISHED'}

	# # assert( len(bone_names) == len(data.bones_frames_eulers) == len(data.bones_frames_locs) )
	# b_action = anim_sys.create_action(b_armature_ob, filename)
	# # go over list of euler keys
	# # for bone_i, bone_name in bones_table:
	# # 	b_empty_ob = create_ob(scene, bone_name, None)
	# # 	b_empty_ob.scale = (0.01, 0.01, 0.01)
	# # 	for frame_i in range(bani.data.num_frames):
	# # 		bpy.context.scene.frame_set(frame_i)
	# # 		euler = data.eulers[frame_i, bone_i]
	# # 		loc = data.locs[frame_i, bone_i]
	# # 		bpy.context.scene.frame_set(frame_i)
	# # 		b_empty_ob.location = loc
	# # 		b_empty_ob.keyframe_insert(data_path="location", frame=frame_i)
	#
	# # every bone is rotated without respect to the parent bone
	# # for the fcurves, we need to store it relative to the parent bone, which is keyframed
	# # to compensate, we have to accumulate the rotations for each frame in a tree-like structure
	# # use blender bone index and children to build the tree structure
	# # then multiply a bone's key with the inverse of its parent's key matrix
	# fcurves_rot = [anim_sys.create_fcurves(b_action, "rotation_quaternion", range(4), None, bone_name) for bone_name in bone_names]
	# child_indices_map = [[pchild["index"] for pchild in pbone.children_recursive] for pbone in p_bones]
	# rest_matrices_armature_space = [b_armature_ob.data.bones[bone_name].matrix_local for bone_name in bone_names]
	#
	# def get_p_index(pbone):
	# 	if pbone:
	# 		return pbone["index"]
	# 	else:
	# 		return None
	#
	# parent_index_map = [get_p_index(pbone.parent) for pbone in p_bones]
	# for frame_i in range(bani.data.num_frames):
	# 	logging.info(f"Frame {frame_i}")
	# 	frame_eulers = [mathutils.Euler([math.radians(k) for k in euler]) for euler in bani.eulers[frame_i]]
	# 	print(frame_eulers)
	# 	frame_keys = [euler.to_matrix().to_4x4() for euler in frame_eulers]
	# 	# frame_keys = [mathutils.Euler([0.0 for k in euler]).to_matrix().to_4x4() for euler in bani.eulers[frame_i]]
	# 	accum_mats = [mathutils.Matrix() for _ in bone_names]
	# 	for key_mat, accum_mat, child_indices, parent_index, fcurves, bind in zip(
	# 			frame_keys, accum_mats, child_indices_map, parent_index_map, fcurves_rot, rest_matrices_armature_space):
	# 		accum_mat @= key_mat
	# 		for i in child_indices:
	# 			accum_mats[i] @= key_mat
	# 		if parent_index is not None:
	# 			rel_mat = accum_mats[parent_index].inverted() @ accum_mat
	# 		else:
	# 			rel_mat = accum_mat
	# 		# the eulers are applied globally to the bone, equivalent to the user doing R+X, R+Y, R+Z for each axis.
	# 		# this expresses the rotation that should be done in blender coordinates about the center of the bone
	# 		space_corrected_rot = global_corr_mat @ rel_mat
	# 		# space_corrected_rot = rel_mat
	#
	# 		# rot_mat is the final armature space matrix of the posed bone
	# 		# rot_mat = space_corrected_rot @ armature_space_matrix
	# 		space_corrected_rot = bind @ space_corrected_rot @ bind.inverted()
	# 		# key = corrector.nif_bind_to_blender_bind(key.to_matrix().to_4x4())\
	# 		key = space_corrected_rot.to_quaternion()
	# 		# key = (global_corr_mat @ key.to_matrix().to_4x4()).to_quaternion()
	# 		anim_sys.add_key(fcurves, frame_i, key, interp_loc)
	# 	# break
	# 	# for bone_i, bone_name in bones_table:
	# 	# 	# get pose pbone
	# 	# 	pbone = b_armature_ob.pose.bones[bone_name]
	# 	# 	# pbone.rotation_mode = "XYZ"
	# 	# 	# data_type = "rotation_euler"
	# 	# 	# get object mode bone
	# 	# 	obone = b_armature_ob.data.bones[bone_name]
	# 	# 	armature_space_matrix = obone.matrix_local
	# 	#
	# 	# 	# bpy.context.scene.frame_set(frame_i)
	# 	# 	euler = bani.eulers[frame_i, bone_i]
	# 	# 	loc = bani.locs[frame_i, bone_i]
	# 	# 	# convert to radians
	# 	# 	# euler = mathutils.Euler([math.radians(k) for k in euler])
	# 	#
	# 	# 	# the eulers are applied globally to the bone, equivalent to the user doing R+X, R+Y, R+Z for each axis.
	# 	# 	# this expresses the rotation that should be done in blender coordinates about the center of the bone
	# 	# 	space_corrected_rot = global_corr_mat @ euler.to_matrix().to_4x4()
	# 	#
	# 	# 	# rot_mat is the final armature space matrix of the posed bone
	# 	# 	rot_mat = space_corrected_rot @ armature_space_matrix
	# 	#
	# 	# 	# for fcurve, k in zip(fcu, e):
	# 	# 	# 	fcurve.keyframe_points.insert(frame_i, k)#.interpolation = "Linear"
	# 	#
	# 	# 	# experiments
	# 	# 	# trans = (global_corr_mat @ mathutils.Vector(loc)) + armature_space_matrix.translation
	# 	#
	# 	# 	# mdl2 vectors: (-x,-z,y)
	# 	# 	# loc = mathutils.Vector((-loc[0], -loc[2], loc[1]))
	# 	# 	loc = mathutils.Vector(loc)
	# 	# 	# trans = (mathutils.Vector(loc)) + armature_space_matrix.translation
	# 	# 	# rot_mat.translation = (space_corrected_rot @ loc) + armature_space_matrix.translation
	# 	# 	# loc_key = (space_corrected_rot @ mathutils.Vector(loc))
	# 	# 	loc_key = (euler.to_matrix().to_4x4() @ loc)
	# 	# 	# loc_key = ( loc @ space_corrected_rot)
	# 	# 	# loc_key = mathutils.Vector((-loc_key[0], -loc_key[2], loc_key[1]))
	# 	# 	# rot_mat.translation = loc_key + armature_space_matrix.translation
	# 	# 	# the ideal translation as calculated by blender
	# 	# 	rot_mat.translation = pbone.matrix.translation
	# 	# 	# print(rot_mat)
	# 	# 	pbone.matrix = rot_mat
	# 	#
	# 	# 	# pbone.keyframe_insert(data_path="rotation_euler", frame=frame_i, group=bone_name)
	# 	# 	# pbone.keyframe_insert(data_path="location", frame=frame_i, group=bone_name)
	# return {'FINISHED'}


def load_old(files=[], filepath="", set_fps=False):
	dirname, filename = os.path.split(filepath)
	data = load_banis(filepath)
	data.read_banis()
	print(data)
	# data 0 has various scales and counts
	anim_length = data.data.animation_length
	num_frames = data.data.num_frames

	fps = int(round(num_frames / anim_length))
	scene = bpy.context.scene
	scene.frame_start = 0
	scene.frame_end = num_frames - 1
	print("Banis fps", fps)
	ob = get_armature(scene)

	bones_table = sorted([(bone["index"], bone.name) for bone in ob.pose.bones])
	bone_names = [tup[1] for tup in bones_table]

	# assert( len(bone_names) == len(data.bones_frames_eulers) == len(data.bones_frames_locs) )
	action = create_anim(ob, filename)
	# animate_empties(anim_sys, bones_table, data, scene, ob)

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

			# break
	return {'FINISHED'}


def animate_empties_old(anim_sys, bones_table, bani, scene, b_armature_ob, filename):
	corrector = Corrector(False)
	print(f"corr {global_corr_mat.to_euler()}")
	# go over list of euler keys
	for i, bone_name in bones_table:
		b_empty_ob = create_ob(scene, f"rest_{bone_name}", None)
		bind = b_armature_ob.data.bones[bone_name].matrix_local
		bind = corrector.blender_bind_to_nif_bind(bind)
		# b_empty_ob.matrix_local = bind.inverted()
		# b_empty_ob.matrix_local = bind.inverted()
		b_empty_ob.location = -bind.translation
		b_empty_ob.scale = (0.01, 0.01, 0.01)
	for i, bone_name in bones_table:
		b_empty_ob = create_ob(scene, bone_name, None)
		b_empty_ob.rotation_mode = "QUATERNION"
		b_action = anim_sys.create_action(b_empty_ob, f"{filename}.{bone_name}")
		bind = b_armature_ob.data.bones[bone_name].matrix_local
		bind = corrector.blender_bind_to_nif_bind(bind)
		inv_bind = bind.inverted()
		bind_loc = b_armature_ob.data.bones[bone_name].matrix_local.translation
		# bind_loc_inv = bind_loc.negate()
		# fcurves_rot = anim_sys.create_fcurves(b_action, "rotation_quaternion", range(4), None, bone_name)
		# fcurves_loc = anim_sys.create_fcurves(b_action, "location", range(3), None, bone_name)
		# just object fcurves for now
		fcurves_rot = anim_sys.create_fcurves(b_action, "rotation_quaternion", range(4))
		fcurves_loc = anim_sys.create_fcurves(b_action, "location", range(3))
		# logging.info(f"Bone {bone_name} as empty, bind at {bind_loc}")
		for frame_i in range(bani.data.num_frames):
			euler = bani.eulers[frame_i, i]
			euler = mathutils.Euler([math.radians(k) for k in euler])
			rot = global_corr_mat @ euler.to_matrix().to_4x4()
			if frame_i == 0:
				print(f"{i} {euler} | {rot.to_euler()}")
			loc = bani.locs[frame_i, i]
			# this seems to be absolutely correct for JWE2 tuna
			loc = mathutils.Vector((loc[0], loc[2], -loc[1]))
			# loc = mathutils.Vector(loc)
			# the translation key is rotated about bind_loc mirrored on the origin
			# first add bind_loc so that the origin of rotation is at the origin
			corr = loc + bind_loc
			# rotate by the euler key
			corr.rotate(rot.inverted())
			# corr.rotate(e_fixed)
			# go back to pose position
			loc_final = corr - bind_loc

			# euler y and z need to be negated
			e_fixed = rot.to_euler()
			e_fixed = mathutils.Euler((e_fixed[0], -e_fixed[1], -e_fixed[2]))
			rot_final = e_fixed.to_quaternion()

			# # assuming the transform is stored relative to the inverse skin bind transform
			# # some attempts, no success yet
			# euler = bani.eulers[frame_i, i]
			# loc = bani.locs[frame_i, i]
			# euler = mathutils.Euler([math.radians(k) for k in euler])
			# key = global_corr_mat @ euler.to_matrix().to_4x4()
			# # key = euler.to_matrix().to_4x4()
			# key.translation = loc
			# # key = inv_bind @ key.inverted() @ bind
			# # key = bind @ key.inverted() @ inv_bind
			# # key = inv_bind @ key @ bind
			# # key = bind @ key @ inv_bind
			# key = key
			# # key = bind @ inv_bind
			# rot_final = key.to_quaternion()
			# loc_final = key.translation
			anim_sys.add_key(fcurves_rot, frame_i, rot_final, interp_loc)
			anim_sys.add_key(fcurves_loc, frame_i, loc_final, interp_loc)
		b_empty_ob.scale = (0.01, 0.01, 0.01)


def animate_empties(anim_sys, bones_table, bani, scene, b_armature_ob):
	"""trying to work with uncorrected"""
	corrector = Corrector(False)
	print(f"corr {global_corr_mat.to_euler()}")
	binds = []
	fcurves_rot = []
	fcurves_loc = []
	# create the fcurves and empties if needed
	use_armature = False
	if use_armature:
		b_action = anim_sys.create_action(b_armature_ob, bani.name)
	for bone_i, bone_name in bones_table:
		bind = b_armature_ob.data.bones[bone_name].matrix_local
		bind = corrector.blender_bind_to_nif_bind(bind)
		# inv_bind = bind.inverted()
		# bind_loc = b_armature_ob.data.bones[bone_name].matrix_local.translation
		# bind_loc_inv = bind_loc.negate()
		binds.append(bind)

		# create new empty
		if not use_armature:
			b_empty_ob = create_ob(scene, bone_name, None)
			b_empty_ob.rotation_mode = "QUATERNION"
			b_empty_ob.scale = (0.01, 0.01, 0.01)
			b_action = anim_sys.create_action(b_empty_ob, f"{bani.name}.{bone_name}")
		# create fcurves
		channel_name = bone_name if use_armature else None
		fcurves_rot.append(anim_sys.create_fcurves(b_action, "rotation_quaternion", range(4), None, channel_name))
		fcurves_loc.append(anim_sys.create_fcurves(b_action, "location", range(3), None, channel_name))

	# go frame per frame
	for frame_i, frame in enumerate(bani.keys):
		matrix_storage = [None for _ in bones_table]
		for bone_i, bone_name in bones_table:
		# logging.info(f"Bone {bone_name} as empty, bind at {bind_loc}")
		# for frame_i in range(len(bani.keys)):
			# euler = bani.eulers[frame_i, i]
			# euler = mathutils.Euler([math.radians(k) for k in euler])
			# rot = global_corr_mat @ euler.to_matrix().to_4x4()
			# if frame_i == 0:
			# 	print(f"{i} {euler} | {rot.to_euler()}")
			# loc = bani.locs[frame_i, i]
			# # this seems to be absolutely correct for JWE2 tuna
			# # loc = mathutils.Vector((loc[0], loc[2], -loc[1]))
			# loc = mathutils.Vector(loc)
			# # the translation key is rotated about bind_loc mirrored on the origin
			# # first add bind_loc so that the origin of rotation is at the origin
			# corr = loc + bind_loc
			# # rotate by the euler key
			# corr.rotate(rot.inverted())
			# # corr.rotate(e_fixed)
			# # go back to pose position
			# loc_final = corr - bind_loc
			#
			# # euler y and z need to be negated
			# e_fixed = rot.to_euler()
			# # e_fixed = mathutils.Euler((e_fixed[0], -e_fixed[1], -e_fixed[2]))
			# rot_final = e_fixed.to_quaternion()

			# assuming the transform is stored relative to the inverse skin bind transform
			# some attempts, no success yet
			euler = frame["euler"][bone_i]
			loc = frame["loc"][bone_i]
			euler = mathutils.Euler([math.radians(k) for k in euler])
			rot = global_corr_mat @ euler.to_matrix().to_4x4()
			key = global_corr_mat @ euler.to_matrix().to_4x4()
			# key = euler.to_matrix().to_4x4()
			key.translation = loc
			# key = inv_bind @ key.inverted() @ bind
			# key = bind @ key.inverted() @ inv_bind
			# key = inv_bind @ key @ bind
			# key = bind @ key @ inv_bind
			# this maybe adds the loc transforms, doesn't seem to correctly transform rot ??
			key = key @ binds[bone_i]
			# store the posed armature space matrix
			matrix_storage[bone_i] = corrector.nif_bind_to_blender_bind(key)

		# todo - make posed armature space matrices relative to posed parent
		#  make that relative to local bind

		for bone_i, bone_name in bones_table:
			key = matrix_storage[bone_i]
			rot_final = key.to_quaternion()
			loc_final = key.translation
			anim_sys.add_key(fcurves_rot[bone_i], frame_i, rot_final, interp_loc)
			anim_sys.add_key(fcurves_loc[bone_i], frame_i, loc_final, interp_loc)
