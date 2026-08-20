import os
import logging
import time
from typing import Optional, TYPE_CHECKING

import bpy
import mathutils
import numpy as np

from generated.formats.bani import BanisFile
from plugin.modules_export.armature import get_armature
from plugin.modules_import.anim import Animation
from plugin.utils.anim import get_bone_bind_data
from plugin.utils.transforms import Corrector
from plugin.utils.object import get_bones_table, get_parent_map
if TYPE_CHECKING:
	from generated.formats.bani.structs.BaniInfo import BaniInfo

interp_loc = None


def load(reporter, files=(), filepath="", set_fps=False):
	start_time = time.time()
	in_dir, banis_name = os.path.split(filepath)
	scene = bpy.context.scene
	b_main_armature_ob = get_armature(scene.objects)
	b_armatures_map = {ob.name: ob for ob in scene.objects if type(ob.data) == bpy.types.Armature}

	bones_table, p_bones = get_bones_table(b_main_armature_ob)
	logging.debug("\n[DEBUG] --- Bone Mapping ---")
	for bone_i, b_bone_name in bones_table:
		logging.debug(f"  MS2 Bone Index {bone_i} -> Bone: '{b_bone_name}'")

	parent_index_map = get_parent_map(p_bones)
	anim_sys = Animation()
	banis = BanisFile()
	banis.load(filepath)

	for bani in banis.anims:
		logging.debug(f"'{bani.name}', flag: {bani.data.flags}")
		# select target armature for pose anims of PZ1 animals with decimated skeletons
		b_target_armature = b_main_armature_ob
		if "_pose_" in bani.name:
			arm_name = bani.name.replace("_idle", "") + "_armature"
			b_target_armature = b_armatures_map.get(arm_name, b_main_armature_ob)
		animate_core(anim_sys, bones_table, bani, b_main_armature_ob, b_target_armature, parent_index_map)

	reporter.show_info(f"Imported {banis_name} in {time.time()-start_time:.2f} s")


def animate_core(anim_sys: Animation, bones_table: list[tuple[int, str]], bani: 'BaniInfo', b_main_armature_ob, b_target_armature, parent_index_map):
	# Fetch the animation mode defined by the flag (1=Absolute, 2=Relative, 3=Additive, 5=Version < 7)
	anim_mode = bani.data.mode if bani.context.version >= 7 else 5

	corrector = Corrector(False)

	b_action = anim_sys.create_action(b_target_armature, bani.name)
	# store fps on action to retrieve it and set to the scene when changing actions
	b_action["fps"] = int(round((bani.data.num_frames - 1) / bani.data.animation_length))
	if b_main_armature_ob == b_target_armature:
		g_bind_armature_space, b_bind_local_space = get_bone_bind_data(b_main_armature_ob, bones_table, corrector)
	else:
		# main armature's bind is actually in rest pose
		g_bind_armature_space, _ = get_bone_bind_data(b_main_armature_ob, bones_table, corrector)
		# target armature's bind is already posed
		_, b_bind_local_space = get_bone_bind_data(b_target_armature, bones_table, corrector)

	# Fetch the list of bones that are actually animated in this file
	animated_bone_indices = set(getattr(bani, "animated_bone_indices", range(len(bones_table))))
	if anim_mode == 5:
		animated_bone_indices = set(i for i, b_bone_name in bones_table if b_bone_name in b_target_armature.pose.bones)
	is_partial = len(animated_bone_indices) < len(bones_table)

	g_posed_armature_space: list[Optional[mathutils.Matrix]] = [None for _ in bones_table]
	b_posed_armature_space: list[Optional[mathutils.Matrix]] = [None for _ in bones_table]
	b_posed_local_space: list[Optional[mathutils.Matrix]] = [None for _ in bones_table]
	b_posed_delta_locs = np.empty_like(bani.locs)
	b_posed_delta_quats = np.empty_like(bani.quats)
	# go frame per frame
	for frame_i in range(bani.data.num_frames):

		for bone_i, b_bone_name in bones_table:
			# Un-animated bones will receive (1,0,0,0) and (0,0,0) here, mapping safely to Bind Pose.
			g_key: mathutils.Matrix = mathutils.Quaternion(bani.quats[frame_i, bone_i]).to_matrix().to_4x4()
			g_key.translation = bani.locs[frame_i, bone_i]

			# Fetch the readIdx for this bone
			read_i = getattr(bani, "read_mapping", {}).get(bone_i, 255)

			parent_i = parent_index_map[bone_i] if read_i == 255 else read_i

			# Blend Modes
			if anim_mode == 1:
				# MODE 1 (Absolute): Keys are fully baked to world space. Ignore parent.
				g_posed_armature_space[bone_i] = g_key

			elif anim_mode == 2:
				# MODE 2 Relative/FK
				if is_partial and parent_i is not None:
					# 0 = Root bone, attached to spine. For Walk Partials 0 is the actual read_i, yet it blows up
					# -1 (SRB) works for Walk Partials, read_i/parent_i *does not*
					g_posed_armature_space[bone_i] = g_bind_armature_space[-1] @ g_key
				else:
					# Mode 2 I have looked at don't get here
					g_posed_armature_space[bone_i] = g_key  # Maybe g_bind_armature_space[bone_i] @ g_key

			elif anim_mode == 3:
				# MODE 3: Additive
				if is_partial:
					g_posed_armature_space[bone_i] = g_key @ g_bind_armature_space[bone_i]
				else:
					# TODO: Blows up, `g_key @ g_bind_armature_space[bone_i]` doesn't work either
					# bodyflume_bendup, bodyflume_benddown
					# Non-partial, 1:1 bone mapping, read_i==255 (None)
					# Not reassigning parent_i also blows up
					parent_i = None if read_i == 255 else parent_i
					g_posed_armature_space[bone_i] = g_bind_armature_space[bone_i] @ g_key

			elif anim_mode == 5:
				# Mode 5: Legacy (Version < 7)
				g_posed_armature_space[bone_i] = g_key @ g_bind_armature_space[bone_i]
				# n.b. for reduced anims, this is not in posed armature space because the bind pose is posed
			
			# Convert posed armature space from game to blender coordinates
			b_posed_armature_space[bone_i] = corrector.to_blender(g_posed_armature_space[bone_i])

		for bone_i, parent_i in enumerate(parent_index_map):
			# Make posed armature-space transform relative to the posed parent bone
			if parent_i is not None:
				b_posed_local_space[bone_i] = b_posed_armature_space[parent_i].inverted() @ b_posed_armature_space[bone_i]
			else:
				b_posed_local_space[bone_i] = b_posed_armature_space[bone_i]

		for bone_i, b_bone_name in bones_table:
			# Skip pushing keyframes to Blender if the curve is un-animated
			if bone_i not in animated_bone_indices:
				continue
			# Factor out Blender's natural Rest Pose to create pure Delta F-Curves
			b_posed_delta_space = b_bind_local_space[bone_i].inverted() @ b_posed_local_space[bone_i]
			b_posed_delta_quats[frame_i, bone_i] = b_posed_delta_space.to_quaternion()
			b_posed_delta_locs[frame_i, bone_i] = b_posed_delta_space.translation

	frames = np.arange(bani.data.num_frames)
	q_range = tuple(range(4))
	l_range = tuple(range(3))
	for bone_i, b_bone_name in bones_table:
		if bone_i in animated_bone_indices:
			anim_sys.add_keys(b_action, "rotation_quaternion", q_range, None, frames, b_posed_delta_quats[:, bone_i], None, n_bone=b_bone_name)
			anim_sys.add_keys(b_action, "location", l_range, None, frames, b_posed_delta_locs[:, bone_i], None, n_bone=b_bone_name)
