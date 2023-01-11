import logging

import bpy
import mathutils

from generated.formats.ms2.compounds.Bone import Bone
from generated.formats.ms2.compounds.Matrix44 import Matrix44
from generated.formats.ms2.versions import is_ztuac, is_dla
from plugin.modules_export.collision import export_hitcheck
from plugin.utils.matrix_util import bone_name_for_ovl, get_joint_name, Corrector
from plugin.utils.shell import get_collection


def get_level(bones, level=0):
	level_children = []
	for bone in bones:
		# print(f"Level {level} {bone.name}")
		if level == 0:
			tmp_children = sorted(bone.children, key=lambda b: bone_name_for_ovl(b.name), reverse=True)

		else:
			tmp_children = sorted(bone.children, key=lambda b: bone_name_for_ovl(b.name))
		level_children.extend(tmp_children)
	return level_children


def ovl_bones_jwe(b_armature_ob):
	b_armature_data = b_armature_ob.data
	# first just get the roots, then extend it
	roots = [bone for bone in b_armature_data.bones if not bone.parent]
	out_bones = []
	level_children = list(roots)
	i = 0
	while level_children:
		# print(level_children)
		out_bones.extend(level_children)
		level_children = get_level(level_children, level=i)
		i += 1
	return [b.name for b in out_bones]


def get_bone_names_from_armature(b_armature_ob):
	assign_p_bone_indices(b_armature_ob)
	sorted_bones = sorted(b_armature_ob.pose.bones, key=lambda p_bone: p_bone["index"])
	return [p_bone.name for p_bone in sorted_bones]
	# return [p_bone.name for p_bone in b_armature_ob.pose.bones]


def assign_p_bone_indices(b_armature_ob):
	print("assigning pbone indices")
	# map index to name to track duplicated indices
	indices = {}
	for p_bone in b_armature_ob.pose.bones:
		if "index" in p_bone:
			p_ind = p_bone["index"]
			if p_ind not in indices:
				indices[p_ind] = p_bone.name
			else:
				raise IndexError(f"Bone {p_bone.name} uses same bone index as {indices[p_ind]}")
	bones_with_index = [p_bone for p_bone in b_armature_ob.pose.bones if "index" in p_bone]
	bones_with_index.sort(key=lambda p_bone: p_bone["index"])
	bones_without_index = [p_bone for p_bone in b_armature_ob.pose.bones if "index" not in p_bone]
	max_index = bones_with_index[-1]["index"]
	print(max_index)
	for p_bone in bones_without_index:
		max_index += 1
		p_bone["index"] = max_index
		print(f"{p_bone.name} = {max_index}")


def get_armature(scene):
	src_armatures = [ob for ob in scene.objects if type(ob.data) == bpy.types.Armature]
	# do we have armatures?
	if src_armatures:
		# see if one of these is selected
		if len(src_armatures) > 1:
			sel_armatures = [ob for ob in src_armatures if ob.select_get()]
			if sel_armatures:
				return sel_armatures[0]
		return src_armatures[0]


def handle_transforms(ob, me, apply=True):
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
			logging.warning(f"{ob.name} has had its object transforms applied on the fly to avoid ingame distortion!")
		else:
			# we simply ignore the transforms and export the mesh as is, but warn the user
			logging.warning(
				f"Ignored object transforms for {ob.name} - orientation will not match what you see in blender!\n"
				f"Check 'Apply Transforms' on export or apply them manually with CTRL+A!")


def export_bones_custom(b_armature_ob, model_info):
	is_old_orientation = is_ztuac(model_info.context) or is_dla(model_info.context)
	corrector = Corrector(is_old_orientation)
	# both options below crash JWE2 instantly, might be due to bone count though
	# b_bone_names = ovl_bones_jwe(b_armature_ob)
	b_bone_names = [bone.name for bone in b_armature_ob.data.bones]
	# now get bone names from b_tex.data
	# if is_jwe(model_info.context):
	# 	b_bone_names = ovl_bones_jwe(b_armature_ob)
	# else:
	# 	b_bone_names = get_bone_names_from_armature(b_armature_ob)
	bone_info = model_info.bone_info
	# update counts
	bone_info.joints.bone_count = bone_info.bind_matrix_count = bone_info.bone_count = \
		bone_info.name_count = bone_info.parents_count = bone_info.enum_count = len(b_bone_names)
	bone_info.reset_field("bones")
	bone_info.reset_field("inverse_bind_matrices")
	bone_info.reset_field("parents")
	bone_info.reset_field("name_indices")
	bone_info.reset_field("enumeration")

	lut_dic = {b_bone_name: bone_index for bone_index, b_bone_name in enumerate(b_bone_names)}
	for bone_i, b_bone_name in enumerate(b_bone_names):
		b_bone = b_armature_ob.data.bones.get(b_bone_name)

		# todo - the correction function works, but only in armature space; come up with one that works in local space to reduce overhead
		mat_local = corrector.blender_bind_to_nif_bind(b_bone.matrix_local)
		# make relative to parent
		if b_bone.parent:
			mat_local_to_parent = corrector.blender_bind_to_nif_bind(b_bone.parent.matrix_local).inverted() @ mat_local
		else:
			mat_local_to_parent = mat_local

		ms2_bone = bone_info.bones[bone_i]
		ms2_bone.name = bone_name_for_ovl(b_bone_name)
		# set parent index
		if b_bone.parent:
			bone_info.parents[bone_i] = lut_dic[b_bone.parent.name]
		else:
			bone_info.parents[bone_i] = 255
		ms2_bone.set_bone(mat_local_to_parent)
		bone_info.inverse_bind_matrices[bone_i].set_rows(mat_local.inverted())

	if bone_info.zeros_count:
		bone_info.zeros_count = len(b_bone_names)
		bone_info.zeros_padding.arg = bone_info.zeros_count
	# paddings are taken care of automatically during writing
	for i in range(len(b_bone_names)):
		bone_info.enumeration[i] = [4, i]

	update_ik_pointers(bone_info)
	export_joints(bone_info, corrector)


def update_ik_pointers(bone_info):
	logging.info("Updating IK pointers")
	bones_map = {bone.name: bone for bone in bone_info.bones}
	for ptr in bone_info.ik_info.get_pointers():
		ptr.joint = bones_map.get(ptr.joint.name)


def export_joints(bone_info, corrector):
	logging.info("Exporting joints")
	scene = bpy.context.scene
	joint_coll = get_collection(f"{scene.name}_joints")
	if not joint_coll:
		return
	joints = bone_info.joints
	# bone_info.joint_count = joints.joint_count = len(joint_coll.objects)
	# joints.reset_field("joint_transforms")
	# joints.reset_field("rigid_body_pointers")
	# joints.reset_field("rigid_body_list")
	# joints.reset_field("joint_infos")
	# make sure these have the correct size
	joints.reset_field("joint_to_bone")
	joints.reset_field("bone_to_joint")
	# reset bone -> joint mapping since we don't catch them all if we loop over existing joints
	joints.bone_to_joint[:] = -1
	joint_map = {get_joint_name(b_ob): b_ob for b_ob in joint_coll.objects}
	bone_lut = {bone.name: bone_index for bone_index, bone in enumerate(bone_info.bones)}
	for joint_i, joint_info in enumerate(joints.joint_infos):
		bone_i = bone_lut[joint_info.bone_name]
		joints.joint_to_bone[joint_i] = bone_i
		joints.bone_to_joint[bone_i] = joint_i
		b_joint = joint_map.get(joint_info.name)
		if not b_joint:
			raise AttributeError(f"Could not find '{joint_info.name}'. Make sure the joint object exists and has the custom property 'long_name' correctly set")
		logging.debug(f"joint {b_joint.name}")
		joint_info.hitcheck_count = len(b_joint.children)
		joint_info.reset_field("hitchecks")
		joint_info.reset_field("hitcheck_pointers")
		for hitcheck, b_hitcheck in zip(joint_info.hitchecks, b_joint.children):
			hitcheck.collision_ignore = b_hitcheck["collision_ignore"]
			hitcheck.collision_use = b_hitcheck["collision_use"]
			hitcheck.name = get_joint_name(b_hitcheck)
			export_hitcheck(b_hitcheck, hitcheck, corrector)
