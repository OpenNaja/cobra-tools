import math
import os
import logging
from typing import Optional, TYPE_CHECKING

import bpy
import mathutils

from generated.formats.bani import BanisFile
from plugin.modules_export.armature import get_armature
from plugin.modules_import.anim import Animation
from plugin.utils.anim import get_bone_bind_data
from plugin.utils.transforms import BanisCorrector, Corrector
from plugin.utils.object import create_ob, get_bones_table, get_parent_map
if TYPE_CHECKING:
	from generated.formats.bani.structs.BaniInfo import BaniInfo

interp_loc = None


def load(reporter, files=(), filepath="", set_fps=False):
	in_dir, banis_name = os.path.split(filepath)
	scene = bpy.context.scene
	b_main_armature_ob = get_armature(scene.objects)
	b_armatures_map = {ob.name: ob for ob in scene.objects if type(ob.data) == bpy.types.Armature}

	bones_table, p_bones = get_bones_table(b_main_armature_ob)
	logging.debug("\n[DEBUG] --- Bone Mapping ---")
	for bone_i, bone_name in bones_table:
		logging.debug(f"  MS2 Bone Index {bone_i} -> Bone: '{bone_name}'")

	parent_index_map = get_parent_map(p_bones)
	anim_sys = Animation()
	banis = BanisFile()
	banis.load(filepath)

	for bani in banis.anims:
		anim_length = bani.data.animation_length
		num_frames = bani.data.num_frames

		scene.frame_start = 0
		scene.frame_end = num_frames-1

		# fps = int(round((num_frames - 1) / anim_length))  # manis uses num_frames - 1
		fps = int(round(num_frames/anim_length))
		scene.render.fps = fps
		logging.debug(f"'{bani.name}' - FPS: {fps}")
		# select target armature for pose anims of PZ1 animals with decimated skeletons
		b_target_armature = b_main_armature_ob
		if "_pose_" in bani.name:
			arm_name = bani.name.replace("_idle", "") + "_armature"
			b_target_armature = b_armatures_map.get(arm_name, b_main_armature_ob)
		animate_core(anim_sys, bones_table, bani, b_main_armature_ob, b_target_armature, parent_index_map)

	reporter.show_info(f"Imported {banis_name}")


def animate_core(anim_sys: Animation, bones_table: list[tuple[int, str]], bani: 'BaniInfo', b_armature_ob, b_target_armature, parent_index_map):
	# Fetch the animation mode defined by the flag (1=Absolute, 2=Relative, 3=Additive, 5=Version < 7)
	anim_mode = bani.data.mode if bani.context.version >= 7 else 5

	corrector = Corrector(False)

	fcurves_rot = []
	fcurves_loc = []

	b_action = anim_sys.create_action(b_target_armature, bani.name)

	# GAME-SPACE BINDS
	binds, bones_local_mat = get_bone_bind_data(b_armature_ob, bones_table, corrector)

	# Fetch the list of bones that are actually animated in this file
	animated_bone_indices = set(getattr(bani, "animated_bone_indices", range(len(bones_table))))
	if anim_mode == 5:
		animated_bone_indices = set(i for i, bone_name in bones_table if bone_name in b_target_armature.pose.bones)
	is_partial = len(animated_bone_indices) < len(bones_table)

	scale_multiplier = 1.0
	# We only apply scale correction on full-body animations
	if anim_mode in (1, ) and not is_partial and len(bones_table) > 1:
		# TODO: Find longest hard bone
		# Pick two bones that define a solid, non-stretching segment of the rig (e.g. Root to Hips).
		bone_a_idx = 0  # Example: Root
		bone_b_idx = 1  # Example: Hips

		# Get the distance in native 1.0x Blender rest pose
		rest_pos_a = binds[bone_a_idx].translation
		rest_pos_b = binds[bone_b_idx].translation
		rest_dist = (rest_pos_b - rest_pos_a).length

		# Get the distance in the raw .banis absolute coordinates at Frame 0
		anim_pos_a = mathutils.Vector(bani.keys[0]["loc"][bone_a_idx])
		anim_pos_b = mathutils.Vector(bani.keys[0]["loc"][bone_b_idx])
		anim_dist = (anim_pos_b - anim_pos_a).length

		# Calculate the scalar required to conform the anim to the rest pose
		if anim_dist > 0.0001:  # Prevent divide-by-zero on collapsed rigs
			scale_multiplier = rest_dist / anim_dist
		logging.debug(f"'{bani.name}' - Scaling Multiplier: {scale_multiplier}")

	for bone_i, bone_name in bones_table:

		# Do not create F-Curves if the bone has no keyframes in this partial animation
		if bone_i not in animated_bone_indices:
			fcurves_rot.append(None)
			fcurves_loc.append(None)
			continue

		fcurves_rot.append(anim_sys.create_fcurves(b_action, "rotation_quaternion", range(4), None, bone_name))
		fcurves_loc.append(anim_sys.create_fcurves(b_action, "location", range(3), None, bone_name))

	# go frame per frame
	for frame_i, frame in enumerate(bani.keys):
		game_armature_space: list[Optional[mathutils.Matrix]] = [None for _ in bones_table]
		posed_armature_space: list[Optional[mathutils.Matrix]] = [None for _ in bones_table]
		posed_local_space: list[Optional[mathutils.Matrix]] = [None for _ in bones_table]

		for bone_i, bone_name in bones_table:
			# Un-animated bones will receive (1,0,0,0) and (0,0,0) here, mapping safely to Bind Pose.
			quat_data = frame["quat"][bone_i]
			loc = [c * scale_multiplier for c in frame["loc"][bone_i]]

			quat = mathutils.Quaternion(quat_data)

			key: mathutils.Matrix = quat.to_matrix().to_4x4()
			key.translation = loc

			# Fetch the readIdx for this bone
			read_i = getattr(bani, "read_mapping", {}).get(bone_i, 255)

			parent_i = parent_index_map[bone_i] if read_i == 255 else read_i

			# Blend Modes
			if anim_mode == 1:
				# MODE 1 (Absolute): Keys are fully baked to world space. Ignore parent.
				game_armature_space[bone_i] = key
				posed_armature_space[bone_i] = corrector.to_blender(game_armature_space[bone_i])

			elif anim_mode == 2:
				# MODE 2 Relative/FK
				if is_partial and parent_i is not None:
					# 0 = Root bone, attached to spine. For Walk Partials 0 is the actual read_i, yet it blows up
					# -1 (SRB) works for Walk Partials, read_i/parent_i *does not*
					game_armature_space[bone_i] = binds[-1] @ key
				else:
					# Mode 2 I have looked at don't get here
					game_armature_space[bone_i] = key  # Maybe binds[bone_i] @ key
				posed_armature_space[bone_i] = corrector.to_blender(game_armature_space[bone_i])

			elif anim_mode == 3:
				# MODE 3: Additive
				if is_partial:
					game_armature_space[bone_i] = key @ binds[bone_i]
				else:
					# TODO: Blows up, `key @ binds[bone_i]` doesn't work either
					# bodyflume_bendup, bodyflume_benddown
					# Non-partial, 1:1 bone mapping, read_i==255 (None)
					# Not reassigning parent_i also blows up
					parent_i = None if read_i == 255 else parent_i
					game_armature_space[bone_i] = binds[bone_i] @ key
				posed_armature_space[bone_i] = corrector.to_blender(game_armature_space[bone_i])

			elif anim_mode == 5:
				# Mode 5: Legacy (Version < 7)
				game_mat = key @ binds[bone_i]
				posed_armature_space[bone_i] = corrector.to_blender(game_mat)

		for bone_i, parent_i in enumerate(parent_index_map):
			if parent_i is not None:
				posed_local_space[bone_i] = posed_armature_space[parent_i].inverted() @ posed_armature_space[bone_i]
			else:
				posed_local_space[bone_i] = posed_armature_space[bone_i]

		for bone_i, bone_name in bones_table:
			# Factor out Blender's natural Rest Pose to create pure Delta F-Curves
			posed_local_space[bone_i] = bones_local_mat[bone_i].inverted() @ posed_local_space[bone_i]

		for bone_i, bone_name in bones_table:
			# Skip pushing keyframes to Blender if the curve is un-animated
			if bone_i not in animated_bone_indices:
				continue

			rot_final = mathutils.Quaternion((1, 0, 0, 0))
			loc_final = mathutils.Vector((0, 0, 0))
			key = posed_local_space[bone_i]
			if key:
				rot_final = key.to_quaternion()
				loc_final = key.translation

			## HACK - When all else fails, ignore translation
			## We allow the Root and its immediate child (Hips) to translate through space.
			## We lock all other limbs to their strict rest lengths so they don't stretch/squish.
			#parent_i = parent_index_map[bone_i]
			#is_root = (parent_i is None)
			#is_hips = (parent_i is not None and parent_index_map[parent_i] is None)
			#
			#if not (is_root or is_hips):
			#	loc_final = mathutils.Vector((0.0, 0.0, 0.0))

			anim_sys.add_key(fcurves_rot[bone_i], frame_i, rot_final, interp_loc)
			anim_sys.add_key(fcurves_loc[bone_i], frame_i, loc_final, interp_loc)

	b_action.use_frame_range = True
	b_action.frame_end = bani.data.num_frames

