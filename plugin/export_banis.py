import logging
import os

import bpy
import mathutils
import numpy as np

from generated.formats.bani import BanisFile
from plugin.modules_export.armature import get_armature
from plugin.utils.anim import get_bone_bind_data
from plugin.utils.transforms import Corrector
from plugin.utils.object import get_bones_table


def save(reporter, filepath=""):
	folder, banis_name = os.path.split(filepath)
	corrector = Corrector(False)
	scene = bpy.context.scene
	b_armature_ob = get_armature(scene.objects)
	if not b_armature_ob:
		logging.warning(f"No armature was found in scene '{scene.name}' - did you delete it?")
		return "Failed, no armature"

	bones_table, p_bones = get_bones_table(b_armature_ob)
	banis = BanisFile()
	banis.num_anims = len(bpy.data.actions)
	banis.reset_field("anims")
	g_bind_mats, b_local_mats = get_bone_bind_data(b_armature_ob, bones_table, corrector)
	# per anim
	for b_action, bani in zip(bpy.data.actions, banis.anims):
		logging.info(f"Exporting {b_action.name}")
		# store pose data for b_action
		b_armature_ob.animation_data.action = b_action
		num_frames = int(round(b_action.frame_range[1] - b_action.frame_range[0]))
		bani.name = b_action.name
		bani.data.banis.pool_index = 0
		bani.data.animation_length = num_frames / scene.render.fps
		bani.keys = np.empty(dtype=banis.dt_float, shape=(num_frames, len(bones_table)))

		# go by frame
		for frame_i, frame in enumerate(bani.keys):
			bpy.context.scene.frame_set(frame_i)
			bpy.context.view_layer.update()
			# sample the frame
			for bone_i, b_bone_name in bones_table:
				p_bone = b_armature_ob.pose.bones[b_bone_name]
				b_posed_armature_space = p_bone.matrix
				# get the posed armature space matrix
				g_posed_armature_space = corrector.from_blender(b_posed_armature_space)
				g_key = g_posed_armature_space @ g_bind_mats[bone_i].inverted()
				frame["loc"][bone_i] = g_key.translation
				frame["quat"][bone_i] = g_key.to_quaternion()

	banis.save(filepath)
	reporter.show_info(f"Exported {banis_name}")
