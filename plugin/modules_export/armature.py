import bpy
import mathutils

from plugin.modules_export.collision import export_hitcheck
from utils import matrix_util


def get_armature():
	src_armatures = [ob for ob in bpy.data.objects if type(ob.data) == bpy.types.Armature]
	# do we have armatures?
	if src_armatures:
		# see if one of these is selected
		if len(src_armatures) > 1:
			sel_armatures = [ob for ob in src_armatures if ob.select_get()]
			if sel_armatures:
				return sel_armatures[0]
		return src_armatures[0]


def handle_transforms(ob, me, errors, apply=True):
	"""Ensures that non-zero object transforms are either applied or reported"""
	# ignore colliders
	if ob.display_type == 'BOUNDS':
		return
	identity = mathutils.Matrix()
	# the world space transform of every rigged mesh must be neutral
	if ob.matrix_local != identity:
		if apply:
			# we only transform the evaluated mesh and leave the actual scene alone
			me.transform(ob.matrix_local)
			errors.append(ob.name + " has had its object transforms applied on the fly to avoid ingame distortion!")
		else:
			# we simply ignore the transforms and export the mesh as is, but warn the user
			errors.append(
				f"Ignored object transforms for {ob.name} - orientation will not match what you see in blender!\n"
				f"Check 'Apply Transforms' on export or apply them manually with CTRL+A!")


def export_bones(b_armature_ob, data):
	b_bone_names = [matrix_util.bone_name_for_blender(n) for n in data.ms2_file.bone_names]
	bone_info = data.ms2_file.bone_info
	for bone_name, ms2_bone, ms2_inv_bind in zip(b_bone_names, bone_info.bones, bone_info.inverse_bind_matrices):
		b_bone = b_armature_ob.data.bones.get(bone_name)
		if not b_bone:
			print(f"Can not update bone {bone_name} because it does not exist in the blender armature")
			continue
		# print(bone_name)
		# print("old: ")
		# print(ms2_inv_bind)
		# print(ms2_bone)

		# todo - the correction function works, but only in armature space; come up with one that works in local space to reduce overhead
		# make relative to parent
		if b_bone.parent:
			mat_local_to_parent = matrix_util.blender_bind_to_nif_bind(b_bone.parent.matrix_local).inverted() @ matrix_util.blender_bind_to_nif_bind(b_bone.matrix_local)
		else:
			mat_local_to_parent = matrix_util.blender_bind_to_nif_bind(b_bone.matrix_local)
		# set the bone transform, relative to parent
		ms2_bone.set_bone(mat_local_to_parent)
		# set the armature space inverse bind pose
		ms2_inv_bind.set_rows(matrix_util.blender_bind_to_nif_bind(b_bone.matrix_local).inverted())

		# print("new: ", )
		# print(ms2_inv_bind)
		# print(ms2_bone)
	export_joints(b_armature_ob, bone_info, b_bone_names)


def export_joints(armature_ob, bone_info, bone_names):
	print("Exporting joints")
	for bone_index, joint_info in zip(bone_info.joints.joint_indices, bone_info.joints.joint_info_list):
		bone_name = bone_names[bone_index]
		print("joint", joint_info.name)
		for hitcheck in joint_info.hit_check:
			b_obj = bpy.data.objects[hitcheck.name]
			export_hitcheck(b_obj, hitcheck)

