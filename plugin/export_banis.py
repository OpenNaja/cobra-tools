import logging
import math
import os

import bpy
import mathutils
import numpy as np

from generated.formats.bani import BanisFile
from plugin.modules_export.armature import get_armature
from plugin.utils.anim import get_bone_bind_data
from plugin.utils.blender_util import get_scale_mat
from plugin.utils.transforms import Corrector
from plugin.utils.object import get_bones_table, get_parent_map


def get_fcurves_by_type(group, dtype):
	return [fcurve for fcurve in group.channels if fcurve.data_path.endswith(dtype)]


def get_groups_for_type(action_groups, dtype):
	out = []
	for group in action_groups:
		fcurves = get_fcurves_by_type(group, dtype)
		assert fcurves
		# todo check correct len
		out.append(fcurves)
	return out


def get_local_bone(bone):
	if bone.parent:
		return bone.parent.matrix_local.inverted() @ bone.matrix_local
	return bone.matrix_local


def save(reporter, filepath=""):
	folder, banis_name = os.path.split(filepath)
	corrector = Corrector(False)
	scene = bpy.context.scene
	bones_data = {}
	b_armature_ob = get_armature(scene.objects)
	if not b_armature_ob:
		logging.warning(f"No armature was found in scene '{scene.name}' - did you delete it?")
		return "Failed, no armature"
	else:
		for bone in b_armature_ob.data.bones:
			bones_data[bone.name] = get_local_bone(bone)

	bones_table, p_bones = get_bones_table(b_armature_ob)
	parent_index_map = get_parent_map(p_bones)
	banis = BanisFile()
	banis.num_anims = len(bpy.data.actions)
	banis.reset_field("anims")
	binds, bones_local_mat = get_bone_bind_data(b_armature_ob, bones_table, corrector)
	# per anim
	for b_action, bani in zip(bpy.data.actions, banis.anims):
		logging.info(f"Exporting {b_action.name}")
		bani.name = b_action.name
		num_frames = int(round(b_action.frame_range[1] - b_action.frame_range[0]))
		bani.data.banis.pool_index = 0
		bani.data.animation_length = num_frames / scene.render.fps
		bani.keys = np.zeros(dtype=banis.dt_float, shape=(num_frames, len(bones_table)))

		# get fcurves
		bone_groups = [b_action.groups[name] for i, name in bones_table]
		loc_groups = get_groups_for_type(bone_groups, "location")
		rot_groups = get_groups_for_type(bone_groups, "rotation_quaternion")
		# go by frame
		for frame_i, frame in enumerate(bani.keys):
			posed_armature_space = [None for _ in bones_table]
			posed_local_space = [None for _ in bones_table]
			# sample the frame
			for bone_i, bone_name in bones_table:
				v = mathutils.Vector([fcu.evaluate(frame_i) for fcu in loc_groups[bone_i]])
				q = mathutils.Quaternion([fcu.evaluate(frame_i) for fcu in rot_groups[bone_i]])
				mat = q.to_matrix().to_4x4()
				mat.translation = v
				posed_local_space[bone_i] = mat

			#  make key relative to local bone bind
			for bone_i, bone_name in bones_table:
				# if frame_i == 50 and bone_name == "def_c_meat11_joint":
				# 	print(bones_local_mat[bone_i])
				# 	print(posed_local_space[bone_i])
				# 	print(bones_local_mat[bone_i] @ posed_local_space[bone_i])
				posed_local_space[bone_i] = bones_local_mat[bone_i] @ posed_local_space[bone_i]
			# make posed armature space matrices relative to posed parent
			for bone_i, parent_i in enumerate(parent_index_map):
				if parent_i is not None:
					# if frame_i in (0, 50) and bone_i == 11:
					# 	print(frame_i)
					# 	print(posed_local_space[bone_i])
					# 	print(posed_local_space[parent_i])
					# 	print(posed_local_space[parent_i] @ posed_local_space[bone_i])
					# 	print(posed_local_space[bone_i] @ posed_local_space[parent_i])
					# nb flipped vs import!!
					posed_armature_space[bone_i] = posed_local_space[parent_i] @ posed_local_space[bone_i]
				else:
					posed_armature_space[bone_i] = posed_local_space[bone_i]
			# take and store the key
			for bone_i, bone_name in bones_table:
				# get the posed armature space matrix
				key = corrector.from_blender(posed_armature_space[bone_i])
				# this maybe adds the loc transforms, doesn't seem to correctly transform rot ??
				# key = binds[bone_i].inverted() @ key
				key = key @ binds[bone_i].inverted()
				# key.translation += binds[bone_i].translation
				frame["loc"][bone_i] = key.translation
				frame["euler"][bone_i] = [math.degrees(v) for v in key.to_euler()]

	banis.save(filepath)
	# print(banis)
	reporter.show_info(f"Exported {banis_name}")
