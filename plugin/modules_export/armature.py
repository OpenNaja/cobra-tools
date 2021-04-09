import bpy
import mathutils

from generated.formats.ms2.compound.JweBone import JweBone
from generated.formats.ms2.compound.Matrix44 import Matrix44
from generated.formats.ovl import is_ztuac
from plugin.modules_export.collision import export_hitcheck
from plugin.modules_import.armature import get_bone_names
from utils import matrix_util
from utils.matrix_util import bone_name_for_ovl


def get_bone_names_from_armature(b_armature_ob):
	assign_p_bone_indices(b_armature_ob)
	sorted_bones = sorted(b_armature_ob.pose.bones, key=lambda p_bone: p_bone["index"])
	return [p_bone.name for p_bone in sorted_bones]
	# return [p_bone.name for p_bone in b_armature_ob.pose.bones]


def assign_p_bone_indices(b_armature_ob):
	print("assigning pbone indices")
	bones_with_index = [p_bone for p_bone in b_armature_ob.pose.bones if "index" in p_bone]
	bones_with_index.sort(key=lambda p_bone: p_bone["index"])
	bones_without_index = [p_bone for p_bone in b_armature_ob.pose.bones if "index" not in p_bone]
	max_index = bones_with_index[-1]["index"]
	print(max_index)
	for p_bone in bones_without_index:
		max_index += 1
		p_bone["index"] = max_index
		print(f"{p_bone.name} = {max_index}")


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


def export_bones_custom(b_armature_ob, data):
	corrector = matrix_util.Corrector(is_ztuac(data))
	# now get bone names from b_armature.data
	b_bone_names = get_bone_names_from_armature(b_armature_ob)
	bone_info = data.ms2_file.bone_info
	# get bone type based on version, or based on bone that previously was used in bones
	if bone_info.bones:
		bone_class = bone_info.bones[0].__class__
	else:
		bone_class = JweBone
	bone_info.bones.clear()
	bone_info.inverse_bind_matrices.clear()
	lut_dic = {b_bone_name: bone_index for bone_index, b_bone_name in enumerate(b_bone_names)}
	# print(lut_dic)
	bone_info.bone_parents.resize(len(b_bone_names))
	for bone_i, b_bone_name in enumerate(b_bone_names):
		b_bone = b_armature_ob.data.bones.get(b_bone_name)

		# todo - the correction function works, but only in armature space; come up with one that works in local space to reduce overhead
		# make relative to parent
		if b_bone.parent:
			mat_local_to_parent = corrector.blender_bind_to_nif_bind(b_bone.parent.matrix_local).inverted() @ corrector.blender_bind_to_nif_bind(b_bone.matrix_local)
		else:
			mat_local_to_parent = corrector.blender_bind_to_nif_bind(b_bone.matrix_local)

		ms2_bone = bone_class()
		ms2_bone.name = bone_name_for_ovl(b_bone_name)
		# set parent index
		if b_bone.parent:
			bone_info.bone_parents[bone_i] = lut_dic[b_bone.parent.name]
		else:
			bone_info.bone_parents[bone_i] = 255
		ms2_bone.set_bone(mat_local_to_parent)

		bone_info.bones.append(ms2_bone)
		ms2_inv_bind = Matrix44()
		ms2_inv_bind.set_rows(corrector.blender_bind_to_nif_bind(b_bone.matrix_local).inverted())
		bone_info.inverse_bind_matrices.append(ms2_inv_bind)

	# update counts
	bone_info.bind_matrix_count = bone_info.bone_count = bone_info.name_count = bone_info.bone_parents_count = \
		bone_info.enum_count = len(b_bone_names)
	bone_info.name_indices.resize(len(b_bone_names))
	# paddings are taken care of automatically during writing
	bone_info.enumeration.resize((len(b_bone_names), 2))
	for i in range(len(b_bone_names)):
		bone_info.enumeration[i] = [4, i]
	# todo - update joints
	# export_joints(b_armature_ob, bone_info, b_bone_names, corrector)


def export_bones(b_armature_ob, data):
	corrector = matrix_util.Corrector(is_ztuac(data))
	b_bone_names = get_bone_names(data)
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
			mat_local_to_parent = corrector.blender_bind_to_nif_bind(b_bone.parent.matrix_local).inverted() @ corrector.blender_bind_to_nif_bind(b_bone.matrix_local)
		else:
			mat_local_to_parent = corrector.blender_bind_to_nif_bind(b_bone.matrix_local)
		# set the bone transform, relative to parent
		ms2_bone.set_bone(mat_local_to_parent)
		# set the armature space inverse bind pose
		ms2_inv_bind.set_rows(corrector.blender_bind_to_nif_bind(b_bone.matrix_local).inverted())

		# print("new: ", )
		# print(ms2_inv_bind)
		# print(ms2_bone)
	export_joints(b_armature_ob, bone_info, b_bone_names, corrector)


def export_joints(armature_ob, bone_info, b_bone_names, corrector):
	print("Exporting joints")
	for bone_index, joint_info in zip(bone_info.joints.joint_indices, bone_info.joints.joint_info_list):
		bone_name = b_bone_names[bone_index]
		print("joint", joint_info.name)
		for hitcheck in joint_info.hit_check:
			b_obj = bpy.data.objects.get(hitcheck.name, None)
			if b_obj:
				export_hitcheck(b_obj, hitcheck, corrector)

