import logging
import math

import bpy
from generated.formats.ms2.enums.RigidBodyFlag import RigidBodyFlag
import mathutils

from generated.formats.ms2.versions import is_ztuac, is_dla
from generated.formats.ms2.compounds.packing_utils import pack_swizzle_collision
from plugin.modules_export.collision import export_hitcheck
from plugin.modules_import.armature import get_matrix
from plugin.utils.matrix_util import bone_name_for_ovl, get_joint_name, Corrector, CorrectorRagdoll
from plugin.utils.object import get_property
from plugin.utils.shell import get_collection_endswith


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
			me.transform(ob.matrix_local, shape_keys=True)
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

	export_ik(b_armature_ob, bone_info)
	export_joints(bone_info, corrector)


def export_ik(b_armature_ob, bone_info):
	logging.debug("Exporting IK")
	bones_with_ik = []
	for p_bone in b_armature_ob.pose.bones:
		if p_bone.constraints:
			b_ik = p_bone.constraints["IK"]
			child_bone = p_bone
			for i in range(b_ik.chain_count):
				bones_with_ik.append((child_bone, child_bone.parent))
				child_bone = p_bone.parent
	bone_info.ik_count = len(bones_with_ik)
	bone_info.reset_field("ik_info")
	# todo ik_targets_count
	ik_info = bone_info.ik_info
	ik_info.ik_count = bone_info.ik_count
	ik_info.reset_field("ik_list")
	bones_map = {bone.name: bone for bone in bone_info.bones}
	for ik_link, (p_child, p_parent) in zip(ik_info.ik_list, bones_with_ik):
		ik_link.parent.joint = bones_map[bone_name_for_ovl(p_parent.name)]
		ik_link.child.joint = bones_map[bone_name_for_ovl(p_child.name)]
		ik_link.yaw.min = -math.degrees(p_child.ik_min_x)
		ik_link.yaw.max = math.degrees(p_child.ik_max_x)
		ik_link.pitch.min = -math.degrees(p_child.ik_min_z)
		ik_link.pitch.max = math.degrees(p_child.ik_max_z)
		# common in PZ eg. penguin
		def_mat = mathutils.Matrix([[-0., 0., 1.], [-0., 1., 0.], [-1, 0., 0.]])
		ik_link.matrix.set_rows(def_mat.transposed())


def export_joints(bone_info, corrector):
	logging.info("Exporting joints")
	scene = bpy.context.scene
	joint_coll = get_collection_endswith(scene, "_joints")
	if not joint_coll:
		return
	joints = bone_info.joints
	bone_info.joint_count = joints.joint_count = len(joint_coll.objects)
	joints.reset_field("joint_transforms")
	joints.reset_field("rigid_body_pointers")
	joints.reset_field("rigid_body_list")
	joints.reset_field("joint_infos")
	joints.reset_field("joint_to_bone")
	joints.reset_field("bone_to_joint")
	# reset bone -> joint mapping since we don't catch them all if we loop over existing joints
	joints.bone_to_joint[:] = -1
	bone_lut = {bone.name: bone_index for bone_index, bone in enumerate(bone_info.bones)}
	for joint_i, joint_info in enumerate(joints.joint_infos):
		b_joint = joint_coll.objects[joint_i]
		joint_info.name = bone_name_for_ovl(get_joint_name(b_joint))
		joint_info.index = joint_i
		joint_info.bone_name = bone_name_for_ovl(b_joint.parent_bone)
		bone_i = bone_lut[joint_info.bone_name]
		joints.joint_to_bone[joint_i] = bone_i
		joints.bone_to_joint[bone_i] = joint_i
		# update joint transform
		b_joint_mat = get_joint_matrix(b_joint)
		n_bind = corrector.blender_bind_to_nif_bind(b_joint_mat)
		t = joints.joint_transforms[joint_i]
		# should not need a transpose but does - maybe change api of set_rows
		t.rot.set_rows(n_bind.to_3x3().inverted().transposed())
		t.loc.set(n_bind.to_translation())

		joint_info.hitcheck_count = len(b_joint.children)
		joint_info.reset_field("hitchecks")
		joint_info.reset_field("hitcheck_pointers")
		version = bpy.context.scene.cobra.version
		for hitcheck, b_hitcheck in zip(joint_info.hitchecks, b_joint.children):
			if version in (48, 50):
				hitcheck.surface_name = b_hitcheck.cobra_coll.surface_pz
				hitcheck.classification_name = b_hitcheck.cobra_coll.classification_pz
			elif version in (51, 52):
				hitcheck.surface_name = b_hitcheck.cobra_coll.surface_jwe2
				hitcheck.classification_name = b_hitcheck.cobra_coll.classification_jwe2
			hitcheck.name = get_joint_name(b_hitcheck)
			export_hitcheck(b_hitcheck, hitcheck, corrector)
		
		rb = joints.rigid_body_list[joint_i]
		if b_joint.children:
			b_rb = b_joint.children[0]
			rb.mass = b_rb.rigid_body.mass
			rb.loc.set(pack_swizzle_collision(b_rb.location))
			rb.air_resistance_x = b_rb.cobra_coll.air_resistance[0]
			rb.air_resistance_y = b_rb.cobra_coll.air_resistance[1]
			rb.air_resistance_z = b_rb.cobra_coll.air_resistance[2]
			rb.unk_1 = b_rb.cobra_coll.damping_3d[0] 
			rb.unk_2 = b_rb.cobra_coll.damping_3d[1]
			rb.unk_4 = b_rb.cobra_coll.damping_3d[2]
			rb.flag = RigidBodyFlag[b_rb.cobra_coll.flag]
		else:
			rb.mass = -1.0
			rb.flag = 0
	# update ragdoll constraints, relies on previously updated joints
	corrector_rag = CorrectorRagdoll(False)
	j_map = {j.name: j for j in joints.joint_infos}
	joints_with_ragdoll_constraints = [b_joint for b_joint in joint_coll.objects if b_joint.rigid_body_constraint]
	joints.num_ragdoll_constraints = len(joints_with_ragdoll_constraints)
	joints.reset_field("ragdoll_constraints")
	for rd, b_joint in zip(joints.ragdoll_constraints, joints_with_ragdoll_constraints):
		rbc = b_joint.rigid_body_constraint
		# get the joint empties, which are the parents of the respective rigidbody objects
		child_joint_name = bone_name_for_ovl(get_joint_name(rbc.object1.parent))
		parent_joint_name = bone_name_for_ovl(get_joint_name(rbc.object2.parent))
		rd.child.joint = j_map[child_joint_name]
		rd.parent.joint = j_map[parent_joint_name]
		rd.child.index = rd.child.joint.index
		rd.parent.index = rd.parent.joint.index
		# update the ragdolls to make sure they point to valid joints
		# rd.parent.joint = j_map[rd.parent.joint.name]
		# rd.child.joint = j_map[rd.child.joint.name]
		rd.loc = joints.joint_transforms[rd.child.joint.index].loc
		# before correcting, rot tends to point y to the child joint
		# the z axis always matches that of the joint empty in blender
		b_joint_mat = get_joint_matrix(b_joint)
		b_joint_mat = b_joint_mat.to_3x3()
		cross = mathutils.Matrix(((0, 0, -1), (0, -1, 0), (-1, 0, 0)))
		b_joint_mat = b_joint_mat @ cross
		b_joint_mat = b_joint_mat.to_4x4()
		n_bind = corrector_rag.blender_bind_to_nif_bind(b_joint_mat)
		# should not need a transpose but does - maybe change api of set_rows
		rd.rot.set_rows(n_bind.to_3x3().inverted().transposed())

		rd.vec_a.set(rd.rot.data[0])
		# note that this is correct for most bones but not all, cf acro
		rd.vec_b.set(rd.rot.data[2])
		rd.x.min = -rbc.limit_ang_x_lower
		rd.x.max = rbc.limit_ang_x_upper
		rd.y.min = -rbc.limit_ang_y_lower
		rd.y.max = rbc.limit_ang_y_upper
		rd.z.min = -rbc.limit_ang_z_lower
		rd.z.max = rbc.limit_ang_z_upper
		# plasticity
		rd.plasticity.min = b_joint.cobra_coll.plasticity_min
		rd.plasticity.max = b_joint.cobra_coll.plasticity_max
	# find the root joint, assuming the first one with least parents
	parents_map = []
	for joint_i, b_joint in enumerate(joint_coll.objects):
		b_bone = b_joint.parent.data.bones[b_joint.parent_bone]
		num_parents = len(b_bone.parent_recursive)
		parents_map.append((num_parents, joint_i))
	parents_map.sort()
	# todo - see how picky this is when there is a joint with root in the name and conflicting root joints
	joints.root_joint_index = parents_map[0][1]


def get_joint_matrix(b_joint):
	b_arm = b_joint.parent
	b_bone = b_arm.data.bones[b_joint.parent_bone]
	# plugin creates mpi that is identity, but can't expect the same case for user generated input
	# depends on how/where it is parented
	# mpi = b_joint.matrix_parent_inverse.inverted()
	# mpi.translation.y -= b_bone.length
	# # relative transform of the joint from the bone
	# joint_mat_local = mpi.inverted() @ b_joint.matrix_basis
	# this works when user applies pose, while the above does not
	joint_mat_local = mathutils.Matrix(b_joint.matrix_local)
	joint_mat_local.translation.y += b_bone.length
	# convert to armature space
	return b_bone.matrix_local @ joint_mat_local

