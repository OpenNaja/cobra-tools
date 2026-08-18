import logging
import os

import bpy
import mathutils
import numpy as np

from generated.formats.bani import BanisFile
from plugin.modules_export.animation import get_actions
from plugin.modules_export.armature import get_armature, get_armatures_collections
from plugin.utils.anim import get_bone_bind_data
from plugin.utils.transforms import Corrector
from plugin.utils.object import get_bones_table


def save(reporter, filepath=""):
	folder, banis_name = os.path.split(filepath)
	corrector = Corrector(False)
	scene = bpy.context.scene

	anim_map = {}
	for b_ob, mdl2_coll in get_armatures_collections(scene):
		if not b_ob:
			logging.warning(f"No armature was found in MDL2 '{mdl2_coll.name}' - did you delete it?")
			continue
		logging.info(f"Exporting actions for {b_ob.name}")
		# animation_data needn't be present on all armatures
		if not b_ob.animation_data:
			logging.info(f"No animation data on '{b_ob.name}'")
			continue
		if b_ob not in anim_map:
			anim_map[b_ob] = set()
		# store actions that are valid for this armature
		anim_map[b_ob].update(get_actions(b_ob))

	all_actions = [action for actions in anim_map.values() for action in actions]

	banis = BanisFile()
	# legacy format
	banis.version = 5
	banis.num_anims = len(all_actions)
	banis.reset_field("anims")
	bani_i = 0
	for b_target_armature, actions in anim_map.items():
		b_armature_ob = b_target_armature
		# find the armature with full skeleton
		if "_pose_" in b_target_armature.name:
			b_armature_ob = [b_ob for b_ob in anim_map if "_pose_" not in b_ob.name][0]
		bones_table, p_bones = get_bones_table(b_armature_ob)
		g_bind_mats, _ = get_bone_bind_data(b_armature_ob, bones_table, corrector)
		# per anim
		for b_action in sorted(actions, key=lambda x: x.name):
			logging.info(f"Exporting {b_action.name} for {b_target_armature.name}")
			# store pose data for b_action
			b_target_armature.animation_data.action = b_action
			num_frames = int(round(b_action.frame_range[1] - b_action.frame_range[0]))

			bani = banis.anims[bani_i]
			bani.name = b_action.name
			bani.data.banis.pool_index = 0
			bani.data.animation_length = (num_frames-1) / scene.render.fps
			bani.keys = np.empty(dtype=banis.dt_float, shape=(num_frames, len(bones_table)))
			bani_i += 1

			# go by frame
			for frame_i, frame in enumerate(bani.keys):
				bpy.context.scene.frame_set(frame_i)
				bpy.context.view_layer.update()
				# sample the frame
				for bone_i, b_bone_name in bones_table:
					# if reduced armature lacks bone, fall back to setting identity transform
					if b_bone_name in b_target_armature.pose.bones:
						p_bone = b_target_armature.pose.bones[b_bone_name]
						b_posed_armature_space = p_bone.matrix
						# get the posed armature space matrix
						g_posed_armature_space = corrector.from_blender(b_posed_armature_space)
						g_key = g_posed_armature_space @ g_bind_mats[bone_i].inverted()
						# todo - find correct transforms for PZ exhibit pose anims with reduced bone counts
						#  note that eyes of frogs are correct relative to head
						#  b_posed_armature_space appears not to match for the reduced versions
						# if "head" in b_bone_name and "_02_" in bani.name and frame_i == 0:
						# 	print(bani.name)
						# 	print(g_key)
						# 	# print(g_bind_mats[bone_i])
						# 	print(b_posed_armature_space)
						# 	# print(g_posed_armature_space[bone_i] @ g_bind_mats[bone_i].inverted())
						frame["loc"][bone_i] = g_key.translation
						frame["quat"][bone_i] = g_key.to_quaternion()
					else:
						frame["loc"][bone_i] = (0, 0, 0)
						frame["quat"][bone_i] = (1., -0., -0., -0.)

	banis.save(filepath)
	reporter.show_info(f"Exported {banis_name}")
