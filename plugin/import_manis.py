import os
import time
import math

import bpy
import mathutils

from generated.formats.manis import ManisFile


def load_manis(file_path):
	"""Loads a manis from the given file path"""
	print("Importing {0}".format(file_path))

	data = ManisFile()
	# open file for binary reading
	data.load(file_path)
	return data


def get_armature():
	src_armatures = [ob for ob in bpy.data.objects if type(ob.data) == bpy.types.Armature]
	#do we have armatures?
	if src_armatures:
		#see if one of these is selected -> get only that one
		if len(src_armatures) > 1:
			sel_armatures = [ob for ob in src_armatures if ob.select_get()]
			if sel_armatures:
				return sel_armatures[0]
		return src_armatures[0]
	
def create_anim(ob, anim_name):
	action = bpy.data.actions.new(name = anim_name)
	action.use_fake_user = True
	ob.animation_data_create()
	ob.animation_data.action = action
	return action

def ovl_bones(b_armature_data):
	# first just get the roots, then extend it
	roots = [bone for bone in b_armature_data.bones if not bone.parent]
	# this_level = []
	out_bones = roots
	# next_level = []
	for bone in roots:
		out_bones += [child for child in bone.children]
	bone_names = [b.name for b in out_bones]
	if "srb" in bone_names:
		bone_names.remove("srb")
		bone_names.append("srb")
	return bone_names
	
def load(operator, context, files = [], filepath = "", set_fps=False):
	starttime = time.clock()
	dirname, filename = os.path.split(filepath)
	data = load_manis(filepath)
	# print(data)
	# # data 0 has various scales and counts
	# anim_length = data.data_0.animation_length
	# num_frames = data.data_0.num_frames
	#
	# global_corr_euler = mathutils.Euler( [math.radians(k) for k in (0,-90,-90)] )
	# global_corr_mat = global_corr_euler.to_matrix().to_4x4()
	#
	# fps = int(round(num_frames/anim_length))
	# bpy.context.scene.frame_start = 0
	# bpy.context.scene.frame_end = num_frames-1
	# print("maniss fps", fps)
	# ob = get_armature()
	#
	# bones_table = [(bone["index"], bone.name) for bone in ob.pose.bones]
	# bone_names = [tup[1] for tup in sorted(bones_table)]

	# ns = ("def_rearLegUpr_joint.L", "def_rearLegUprHalfTwist_joint.L", "def_rearLegUprAllTwist_joint.L",
	# 	  "def_rearLegLwr_joint.L", "def_rearLegLwrHalfTwist_joint.L", "def_rearLegLwrAllTwist_joint.L")
	# # ns = ("def_c_neck_joint", "def_c_head_joint", "def_wing_joint.L", "def_wing02_joint.L", "def_wing_joint.R", "def_wing02_joint.R")
	# # ns = ("def_rearHorselink_joint.L", "def_rearFoot_joint.L", "def_toeRearRing1_joint.L", "def_toeRearRing2_joint.L", "def_toeRearRing3_joint.L",
	# # 	  "def_rearHorselink_joint.R", "def_rearFoot_joint.R", "def_toeRearRing1_joint.R", "def_toeRearRing2_joint.R", "def_toeRearRing3_joint.R")
	#
	# # a rotation is not relative to the parent, but relative to the rest pose
	#
	# for n in ns:
	# 	i = bone_names.index(n)
	# 	euler = data.eulers[0, i]
	# 	# loc = data.locs[:, i]
	# 	loc = data.locs[0, i]
	# 	print(n, "euler", euler)
	# 	print(n, "locat", loc)
	# return
	# bone_names = ovl_bones(ob.data)
	# goliath imports fine with the correct name order
	# bone_names = ['def_c_root_joint', 'def_c_hips_joint', 'def_c_spine1_joint', 'def_c_spine2_joint', 'def_c_chestBreath_joint', 'def_c_spine3_joint', 'def_c_chest_joint', 'def_c_neck1_joint', 'def_c_head_joint', 'def_c_jaw_joint', 'def_l_clavicle_joint', 'def_l_frontLegUpr_joint', 'def_l_frontLegLwr_joint', 'def_l_frontFoot_joint', 'def_l_toeFrontIndex1_joint', 'def_l_toeFrontIndex2_joint', 'def_l_toeFrontPinky1_joint', 'def_l_toeFrontPinky2_joint', 'def_l_toeFrontPinky3_joint', 'def_l_toeFrontRing1_joint', 'def_l_toeFrontRing2_joint', 'def_l_toeFrontRing3_joint', 'def_l_frontLegLwrAllTwist_joint', 'def_l_frontLegLwrHalfTwist_joint', 'def_l_frontLegUprAllTwist_joint', 'def_r_clavicle_joint', 'def_r_frontLegUpr_joint', 'def_r_frontLegLwr_joint', 'def_r_frontFoot_joint', 'def_r_toeFrontIndex1_joint', 'def_r_toeFrontIndex2_joint', 'def_r_toeFrontPinky1_joint', 'def_r_toeFrontPinky2_joint', 'def_r_toeFrontPinky3_joint', 'def_r_toeFrontRing1_joint', 'def_r_toeFrontRing2_joint', 'def_r_toeFrontRing3_joint', 'def_r_frontLegLwrAllTwist_joint', 'def_r_frontLegLwrHalfTwist_joint', 'def_r_frontLegUprAllTwist_joint', 'def_l_rearLegUpr_joint', 'def_l_rearLegLwr_joint', 'def_l_rearHorselink_joint', 'def_l_rearFoot_joint', 'def_l_toeRearMid1_joint', 'def_l_toeRearMid2_joint', 'def_l_toeRearMid3_joint', 'def_l_toeRearPinky1_joint', 'def_l_toeRearPinky2_joint', 'def_l_toeRearPinky3_joint', 'def_l_toeRearRing1_joint', 'def_l_toeRearRing2_joint', 'def_l_toeRearRing3_joint', 'def_l_toeRearThumb1_joint', 'def_l_toeRearThumb2_joint', 'def_l_toeRearThumb3_joint', 'def_l_rearLegLwrAllTwist_joint', 'def_l_rearLegLwrHalfTwist_joint', 'def_l_rearLegUprAllTwist_joint', 'def_r_rearLegUpr_joint', 'def_r_rearLegLwr_joint', 'def_r_rearHorselink_joint', 'def_r_rearFoot_joint', 'def_r_toeRearMid1_joint', 'def_r_toeRearMid2_joint', 'def_r_toeRearMid3_joint', 'def_r_toeRearPinky1_joint', 'def_r_toeRearPinky2_joint', 'def_r_toeRearPinky3_joint', 'def_r_toeRearRing1_joint', 'def_r_toeRearRing2_joint', 'def_r_toeRearRing3_joint', 'def_r_toeRearThumb1_joint', 'def_r_toeRearThumb2_joint', 'def_r_toeRearThumb3_joint', 'def_r_rearLegLwrAllTwist_joint', 'def_r_rearLegLwrHalfTwist_joint', 'def_r_rearLegUprAllTwist_joint', 'def_c_throat_joint', 'def_l_eyelidUpr_joint', 'def_r_eyelidUpr_joint', 'def_l_toeFrontIndex3_joint', 'def_l_toeFrontThumb1_joint', 'def_l_toeFrontThumb2_joint', 'def_l_toeFrontThumb3_joint', 'def_l_frontLegUprHalfTwist_joint', 'def_r_toeFrontIndex3_joint', 'def_r_toeFrontThumb1_joint', 'def_r_toeFrontThumb2_joint', 'def_r_toeFrontThumb3_joint', 'def_r_frontLegUprHalfTwist_joint', 'def_l_chestBreath_joint', 'def_r_chestBreath_joint', 'def_l_toeRearIndex1_joint', 'def_l_toeRearIndex2_joint', 'def_l_toeRearIndex3_joint', 'def_l_rearLegUprHalfTwist_joint', 'def_r_toeRearIndex1_joint', 'def_r_toeRearIndex2_joint', 'def_r_toeRearIndex3_joint', 'def_r_rearLegUprHalfTwist_joint', 'rig_l_frontToe_joint', 'rig_r_frontToe_joint', 'rig_l_rearToe_joint', 'rig_r_rearToe_joint', 'srb']
	# print(bone_names)
	# print(len(bone_names), len(data.bones_frames_eulers), len(data.bones_frames_locs))
	# assert( len(bone_names) == len(data.bones_frames_eulers) == len(data.bones_frames_locs) )
	# action = create_anim(ob, filename)
	# go over list
	for i, bone_name in enumerate(data.bone_names):
		# print(i, bone_name)

		# bone_keys = data.eulers_dict[bone_name]
		# bone_name = bone_name.decode()
		# get pose pbone
		pass
	return {'FINISHED'}
