import math
import os

import bpy
import mathutils

from generated.formats.bani import BanisFile
from plugin.modules_export.armature import get_armature
from plugin.modules_import.anim import Animation
from plugin.utils.anim import get_bone_bind_data
from plugin.utils.matrix_util import Corrector
from plugin.utils.object import create_ob, get_bones_table, get_parent_map

interp_loc = None
# global_corr_euler = mathutils.Euler([math.radians(k) for k in (0, -90, -90)])
global_corr_euler = mathutils.Euler([math.radians(k) for k in (0, 0, 0)])
# global_corr_euler = mathutils.Euler([math.radians(k) for k in (90, 90, 90)])
global_corr_mat = global_corr_euler.to_matrix().to_4x4()


def load(reporter, files=(), filepath="", set_fps=False):
	in_dir, banis_name = os.path.split(filepath)
	use_armature = True
	scene = bpy.context.scene
	b_armature_ob = get_armature(scene.objects)

	bones_table, p_bones = get_bones_table(b_armature_ob)
	bone_names = [tup[1] for tup in bones_table]

	parent_index_map = get_parent_map(p_bones)
	anim_sys = Animation()
	banis = BanisFile()
	banis.load(filepath)
	print(banis)
	for bani in banis.anims:
		# data 0 has various scales and counts
		anim_length = bani.data.animation_length
		num_frames = bani.data.num_frames

		scene.frame_start = 0
		scene.frame_end = num_frames-1
		fps = int(round(num_frames/anim_length))
		# print(f"Banis fps = {fps}")
		animate_core(anim_sys, bones_table, bani, scene, b_armature_ob, parent_index_map, use_armature)
	if not use_armature:
		for i, bone_name in bones_table:
			b_empty_ob = create_ob(scene, f"rest_{bone_name}", None)
			bind = b_armature_ob.data.bones[bone_name].matrix_local
			# bind = corrector.blender_bind_to_nif_bind(bind)
			# b_empty_ob.matrix_local = bind.inverted()
			# b_empty_ob.matrix_local = bind.inverted()
			b_empty_ob.location = bind.translation
			b_empty_ob.scale = (0.01, 0.01, 0.01)
	reporter.show_info(f"Imported {banis_name}")


def animate_core(anim_sys, bones_table, bani, scene, b_armature_ob, parent_index_map, use_armature=True):
	"""trying to work with uncorrected
	this assumes that bone_i is continuous"""
	corrector = Corrector(False)
	print(f"corr {global_corr_mat.to_euler()}")
	fcurves_rot = []
	fcurves_loc = []
	# create the fcurves and empties if needed
	if use_armature:
		b_action = anim_sys.create_action(b_armature_ob, bani.name)
	binds, bones_local_mat = get_bone_bind_data(b_armature_ob, bones_table, corrector)

	for bone_i, bone_name in bones_table:
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
		posed_armature_space = [None for _ in bones_table]
		posed_local_space = [None for _ in bones_table]
		for bone_i, bone_name in bones_table:
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
			# key.translation += binds[bone_i].translation
			# store the posed armature space matrix
			posed_armature_space[bone_i] = corrector.nif_bind_to_blender_bind(key)
		if use_armature:
			# make posed armature space matrices relative to posed parent
			for bone_i, parent_i in enumerate(parent_index_map):
				if parent_i is not None:
					posed_local_space[bone_i] = posed_armature_space[parent_i].inverted() @ posed_armature_space[bone_i]
				else:
					posed_local_space[bone_i] = posed_armature_space[bone_i]
			#  make that relative to local bone bind
			for bone_i, bone_name in bones_table:
				posed_local_space[bone_i] = bones_local_mat[bone_i].inverted() @ posed_local_space[bone_i]

		for bone_i, bone_name in bones_table:
			key = posed_local_space[bone_i]
			rot_final = key.to_quaternion()
			loc_final = key.translation
			anim_sys.add_key(fcurves_rot[bone_i], frame_i, rot_final, interp_loc)
			anim_sys.add_key(fcurves_loc[bone_i], frame_i, loc_final, interp_loc)


