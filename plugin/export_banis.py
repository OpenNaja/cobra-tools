import logging
import os
from typing import Optional

import bpy
import mathutils
import numpy as np

from generated.formats.bani import BanisFile
from plugin.modules_export.animation import get_actions
from plugin.modules_export.armature import get_armatures_collections
from plugin.utils.anim import get_bone_bind_data
from plugin.utils.transforms import Corrector
from plugin.utils.object import get_bones_table, get_parent_map


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
		b_main_armature_ob = b_target_armature
		# find the armature with full skeleton
		if "_pose_" in b_target_armature.name:
			b_main_armature_ob = [b_ob for b_ob in anim_map if "_pose_" not in b_ob.name][0]
		bones_table, p_bones = get_bones_table(b_main_armature_ob)
		# main armature's bind is actually in rest pose
		g_bind_armature_space, _ = get_bone_bind_data(b_main_armature_ob, bones_table, corrector)
		# target armature's bind is already posed
		_, b_bind_local_space = get_bone_bind_data(b_target_armature, bones_table, corrector)
		# g_posed_armature_space: list[Optional[mathutils.Matrix]] = [None for _ in bones_table]
		b_posed_armature_space: list[Optional[mathutils.Matrix]] = [None for _ in bones_table]
		b_posed_local_space: list[Optional[mathutils.Matrix]] = [None for _ in bones_table]
		parent_index_map = get_parent_map(p_bones)
		# per anim
		for b_action in sorted(actions, key=lambda x: x.name):
			logging.info(f"Exporting {b_action.name} for {b_target_armature.name}")
			# store pose data for b_action
			b_target_armature.animation_data.action = b_action
			num_frames = int(round(b_action.frame_range[1] - b_action.frame_range[0]))
			fps = b_action.get("fps", scene.render.fps)
			bani = banis.anims[bani_i]
			bani.name = b_action.name
			bani.data.banis.pool_index = 0
			bani.data.animation_length = (num_frames-1) / fps
			bani.keys = np.empty(dtype=banis.dt_float, shape=(num_frames, len(bones_table)))
			bani_i += 1

			# sample each frame
			for frame_i, frame in enumerate(bani.keys):
				bpy.context.scene.frame_set(frame_i)
				bpy.context.view_layer.update()
				if b_target_armature == b_main_armature_ob:
					# this shortcut works when target and main armature are the same
					for bone_i, b_bone_name in bones_table:
						p_bone = b_target_armature.pose.bones[b_bone_name]
						b_posed_armature_space = p_bone.matrix
						# get the posed armature space matrix
						g_posed_armature_space = corrector.from_blender(b_posed_armature_space)
						g_key = g_posed_armature_space @ g_bind_armature_space[bone_i].inverted()
						frame["loc"][bone_i] = g_key.translation
						frame["quat"][bone_i] = g_key.to_quaternion()
				else:
					# undo the transforms from import for PZ exhibit pose anims with reduced bone counts
					# because b_posed_armature_space is not actually that on import, as the bind poses differ
					for bone_i, b_bone_name in bones_table:
						if b_bone_name in b_target_armature.pose.bones:
							# reconstruct the delta fcurve space from blender's armature space matrix
							p_bone = b_target_armature.pose.bones[b_bone_name]
							b_bone = p_bone.bone
							if b_bone.parent:
								b_posed_delta_space = b_bone.convert_local_to_pose(
									p_bone.matrix,
									b_bone.matrix_local,
									parent_matrix=p_bone.parent.matrix,
									parent_matrix_local=p_bone.parent.bone.matrix_local,
									invert=True)
							else:
								b_posed_delta_space = b_bone.convert_local_to_pose(p_bone.matrix, b_bone.matrix_local,
													  invert=True)
							# add the target bind back
							b_posed_local_space[bone_i] = b_bind_local_space[bone_i] @ b_posed_delta_space
						else:
							# if reduced armature lacks bone, fall back to setting identity transform
							b_posed_local_space[bone_i] = mathutils.Matrix().to_4x4()
					# build the fake armature space matrix with the
					for bone_i, parent_i in enumerate(parent_index_map):
						if parent_i is not None:
							b_posed_armature_space[bone_i] = b_posed_armature_space[parent_i] @ b_posed_local_space[bone_i]
						else:
							b_posed_armature_space[bone_i] = b_posed_local_space[bone_i]

						g_posed_armature_space = corrector.from_blender(b_posed_armature_space[bone_i])
						g_key = g_posed_armature_space @ g_bind_armature_space[bone_i].inverted()
						frame["loc"][bone_i] = g_key.translation
						frame["quat"][bone_i] = g_key.to_quaternion()

	banis.save(filepath)
	reporter.show_info(f"Exported {banis_name}")
