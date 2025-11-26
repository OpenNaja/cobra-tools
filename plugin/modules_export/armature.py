import logging
import math

import bpy
import mathutils

from generated.formats.ms2.enums.Jwe1Collision import Jwe1Collision
from generated.formats.ms2.enums.Jwe1Surface import Jwe1Surface
from generated.formats.ms2.enums.PcCollision import PcCollision
from generated.formats.ms2.enums.PcSurface import PcSurface
from generated.formats.ms2.enums.RigidBodyFlag import RigidBodyFlag
from generated.formats.ms2.versions import is_ztuac, is_dla
from generated.formats.ms2.structs.packing_utils import pack_swizzle_collision
from plugin.modules_export.collision import export_hitcheck
from plugin.utils.blender_util import bone_name_for_ovl, get_joint_name
from plugin.utils.transforms import Corrector, CorrectorRagdoll


def assign_p_bone_indices(b_armature_ob, max_bones=255):
	"""Assigns new 'index' property to all bones. Order does not match original fdev order, consequently breaks banis,
	which rely on correct order of bones."""
	index_set = {p_bone.get("index", None) for p_bone in b_armature_ob.pose.bones}
	bone_count = len(b_armature_ob.pose.bones)
	if bone_count > max_bones:
		raise IndexError(f"Bone count {bone_count} for {b_armature_ob.name} exceeds limit of {max_bones} bones")
	bone_names = [bone_name_for_ovl(p_bone.name) for p_bone in b_armature_ob.pose.bones]
	if len(bone_names) != len(set(bone_names)):
		raise AttributeError(f"Armature {b_armature_ob.name} has clashing bone names")
	# compare current indices to a fully sampled index list
	full_set = set(range(bone_count))
	if index_set != full_set:
		logging.info("Must assign new pose bone indices (breaks .banis)")
		for i, p_bone in enumerate(b_armature_ob.pose.bones):
			p_bone["index"] = i


def get_armature(objects):
	armatures = [ob for ob in objects if type(ob.data) == bpy.types.Armature]
	# do we have armatures?
	if armatures:
		# see if one of these is selected
		if len(armatures) > 1:
			sel_armatures = [ob for ob in armatures if ob.select_get()]
			if sel_armatures:
				armatures = sel_armatures
			for armature in armatures:
				if "_airliftstraps" not in armature.name:
					return armature
		return armatures[0]


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
	assign_p_bone_indices(b_armature_ob)
	bone_info = model_info.bone_info
	# update counts
	bone_info.joints.bone_count = bone_info.bind_matrix_count = bone_info.bone_count = \
		bone_info.name_count = bone_info.parents_count = bone_info.enum_count = bone_info.zeros_count = len(b_armature_ob.data.bones)
	NO_PARENT = 255
	if model_info.context.version > 47:
		# verified as unused for PZ, JWE2
		bone_info.zeros_count = 0
	# WH, PC2
	if model_info.context.version > 52:
		NO_PARENT = 65535
	bone_info.reset_field("bones")
	bone_info.reset_field("inverse_bind_matrices")
	bone_info.reset_field("parents")
	bone_info.reset_field("name_indices")
	bone_info.reset_field("enumeration")
	bone_info.reset_field("minus_padding")
	bone_info.reset_field("zeros_padding")
	bone_info.reset_field("jwe_3_nibbles")

	sorted_bones = sorted(b_armature_ob.data.bones, key=lambda b_bone: b_armature_ob.pose.bones[b_bone.name]["index"])
	for bone_i, b_bone in enumerate(sorted_bones):
		mat_local, mat_local_to_parent = get_bone_matrices(b_bone, corrector)

		ms2_bone = bone_info.bones[bone_i]
		ms2_bone.name = bone_name_for_ovl(b_bone.name)
		ms2_bone.set_bone(mat_local_to_parent)
		# set parent index
		bone_info.parents[bone_i] = b_armature_ob.pose.bones[b_bone.parent.name]["index"] if b_bone.parent else NO_PARENT
		bone_info.inverse_bind_matrices[bone_i].set_rows(mat_local.inverted())
		# ZTUAC, DLA and JWE3 are 1D
		bone_info.enumeration[bone_i] = [4, bone_i] if 13 < model_info.context.version < 55 else bone_i
	# sanity check for bone hierarchy to verify sorting is correct
	for bone_i, parent_i in enumerate(bone_info.parents):
		if parent_i != NO_PARENT:
			if parent_i > bone_i:
				logging.error(f"Bad hierarchy: {bone_info.bones[bone_i].name} {bone_i} -> {bone_info.bones[parent_i].name} {parent_i}")
		# parent_n = bone_info.bones[parent_i].name if parent_i != NO_PARENT else "None"
		# print(f"{bone_info.bones[bone_i].name} {bone_i} -> {parent_n} {parent_i}")
	# paddings are taken care of automatically during writing
	export_ik(b_armature_ob, bone_info)
	export_joints(bone_info, corrector, b_armature_ob)


def get_bone_matrices(b_bone, corrector):
	# correction function works only in armature space
	mat_local = corrector.from_blender(b_bone.matrix_local)
	# make relative to parent
	if b_bone.parent:
		mat_local_to_parent = corrector.from_blender(b_bone.parent.matrix_local).inverted() @ mat_local
	else:
		mat_local_to_parent = mat_local
	return mat_local, mat_local_to_parent


def add_parents(bones_with_ik, p_bone, count):
	child_bone = p_bone
	for i in range(count):
		bones_with_ik[child_bone] = child_bone.parent
		child_bone = child_bone.parent


def export_ik(b_armature_ob, bone_info):
	logging.debug("Exporting IK")
	bones_with_ik = {}
	bones_with_target = {}

	# first look for IK targets
	for p_bone in b_armature_ob.pose.bones:
		for constraint in p_bone.constraints:
			if constraint.type == "COPY_ROTATION":
				if not constraint.subtarget:
					raise AttributeError(f"Copy Rotation constraint on bone '{p_bone.name}' has no target")
				bones_with_target[p_bone] = constraint.subtarget
				# only if bone actually has IK constraint
				if "IK" in p_bone.constraints:
					logging.debug(f"Adding {p_bone.constraints['IK'].chain_count} tracked IK links for {p_bone.name}")
					add_parents(bones_with_ik, p_bone, p_bone.constraints["IK"].chain_count)
				else:
					logging.warning(f"{p_bone.name} on {b_armature_ob.name} has copy rot, but no IK constraint")
	# bare IK
	for p_bone in b_armature_ob.pose.bones:
		for constraint in p_bone.constraints:
			if constraint.type == "IK":
				if p_bone in bones_with_ik:
					# already processed from an IK with target
					continue
				logging.debug(f"Adding {constraint.chain_count} IK links for {p_bone.name}")
				add_parents(bones_with_ik, p_bone, constraint.chain_count)
	# used like this on acro and acro airlift
	bone_info.ik_count = max(len(bones_with_ik), len(bones_with_target))
	bone_info.reset_field("ik_info")
	if not bone_info.ik_count:
		return
	ik_info = bone_info.ik_info
	ik_info.ik_count = len(bones_with_ik)
	ik_info.ik_targets_count = len(bones_with_target)
	ik_info.reset_field("ik_targets")
	ik_info.reset_field("ik_list")
	bones_map = {bone.name: bone for bone in bone_info.bones}

	def check_ik_name(name):
		try:
			return bones_map[bone_name_for_ovl(name)]
		except:
			raise KeyError(f"Bone '{name}' is used by IK constraints but does not exist")
	for ik_target, (p_end, p_target_name) in zip(ik_info.ik_targets, bones_with_target.items()):
		logging.debug(f"Adding IK target {p_end.name}->{p_target_name}")
		ik_target.ik_end.joint = check_ik_name(p_end.name)
		ik_target.ik_blend.joint = check_ik_name(p_target_name)
	for ik_link, (p_child, p_parent) in zip(ik_info.ik_list, bones_with_ik.items()):
		logging.debug(f"Adding IK constraint {p_parent.name}->{p_child.name}")
		ik_link.parent.joint = check_ik_name(p_parent.name)
		ik_link.child.joint = check_ik_name(p_child.name)
		ik_link.yaw.min = -math.degrees(p_child.ik_min_x)
		ik_link.yaw.max = math.degrees(p_child.ik_max_x)
		ik_link.pitch.min = -math.degrees(p_child.ik_min_z)
		ik_link.pitch.max = math.degrees(p_child.ik_max_z)
		# common in PZ eg. penguin
		def_mat = mathutils.Matrix([[-0., 0., 1.], [-0., 1., 0.], [-1, 0., 0.]])
		ik_link.matrix.set_rows(def_mat.transposed())


def iter_constraints(joint_obs, joints, m_name, b_name, j_map, b_armature_basename):
	joints_with_constraints = [b_joint for b_joint in joint_obs if b_joint.rigid_body_constraint and b_joint.rigid_body_constraint.type == b_name]
	constraints_name = f"{m_name}_constraints"
	setattr(joints, f"num_{constraints_name}", len(joints_with_constraints))
	joints.reset_field(constraints_name)
	m_constraints = getattr(joints, constraints_name)
	for rd, b_joint in zip(m_constraints, joints_with_constraints):
		rbc = b_joint.rigid_body_constraint
		if not (rbc.object1 and rbc.object2):
			raise AttributeError(f"Rigidbody constraint on '{b_joint.name}' lacks references to rigidbody objects")
		# get the joint empties, which are the parents of the respective rigidbody objects
		rd.child.joint = set_joint_ref(b_armature_basename, j_map, rbc.object1, b_joint)
		rd.parent.joint = set_joint_ref(b_armature_basename, j_map, rbc.object2, b_joint)
		rd.child.index = rd.child.joint.index
		rd.parent.index = rd.parent.joint.index
		rd.loc = joints.joint_transforms[rd.child.joint.index].loc
		yield rd, b_joint, rbc


def set_joint_ref(b_armature_basename, j_map, hitcheck, b_joint):
	assert hitcheck.type == "MESH", f"Constraint on {b_joint.name} must point to a mesh, not '{hitcheck.name}' ({hitcheck.type})"
	b_target_joint = hitcheck.parent
	joint_name = bone_name_for_ovl(get_joint_name(b_armature_basename, b_target_joint))
	if joint_name in j_map:
		return j_map[joint_name]
	else:
		raise KeyError(f"Can't find joint '{joint_name}' for {b_joint.name}'s target '{hitcheck.name}'")


def export_joints(bone_info, corrector, b_armature_ob):
	logging.info(f"Exporting joints for {b_armature_ob.name}")
	joint_obs = [ob for ob in b_armature_ob.children if ob.type == "EMPTY"]
	if not joint_obs:
		return
	b_armature_basename = b_armature_ob.name.split("_armature")[0]
	joints = bone_info.joints
	bone_info.joint_count = joints.joint_count = len(joint_obs)
	joints.reset_field("joint_transforms")
	joints.reset_field("rigid_body_pointers")
	joints.reset_field("rigid_body_list")
	joints.reset_field("joint_infos")
	joints.reset_field("joint_to_bone")
	joints.reset_field("bone_to_joint")
	# reset bone -> joint mapping since we don't catch them all if we loop over existing joints
	joints.bone_to_joint[:] = -1
	bone_lut = {bone.name: bone_index for bone_index, bone in enumerate(bone_info.bones)}
	for joint_i, (joint_info, b_joint) in enumerate(zip(joints.joint_infos, joint_obs)):
		joint_info.name = bone_name_for_ovl(get_joint_name(b_armature_basename, b_joint))
		joint_info.index = joint_i
		joint_info.bone_name = bone_name_for_ovl(b_joint.parent_bone)
		try:
			bone_i = bone_lut[joint_info.bone_name]
		except KeyError:
			raise KeyError(f"Joint '{b_joint.name}' is child of bone '{b_joint.parent_bone}', which is missing")
		joints.joint_to_bone[joint_i] = bone_i
		joints.bone_to_joint[bone_i] = joint_i
		# update joint transform
		b_joint_mat = get_joint_matrix(b_joint)
		n_bind = corrector.from_blender(b_joint_mat)
		t = joints.joint_transforms[joint_i]
		# should not need a transpose but does - maybe change api of set_rows
		t.rot.set_rows(n_bind.to_3x3().inverted().transposed())
		t.loc.set(n_bind.to_translation())

		joint_info.hitcheck_count = len(b_joint.children)
		joint_info.reset_field("hitchecks")
		joint_info.reset_field("hitcheck_pointers")
		game = bpy.context.scene.cobra.game
		for hitcheck, b_hitcheck in zip(joint_info.hitchecks, b_joint.children):
			surface_name = b_hitcheck.cobra_coll.get_value(bpy.context, "surface")
			classification_name = b_hitcheck.cobra_coll.get_value(bpy.context, "classification")
			if game == "Jurassic World Evolution":
				hitcheck.surface_name = Jwe1Surface[surface_name]
				hitcheck.classification_name = Jwe1Collision[classification_name]
			elif game == "Planet Coaster":
				hitcheck.surface_name = PcSurface[surface_name]
				hitcheck.classification_name = PcCollision[classification_name]
				surface_2_name = b_hitcheck.cobra_coll.get_value(bpy.context, "surface_2")
				hitcheck.surface_name = PcSurface[surface_2_name]
			else:
				hitcheck.surface_name = surface_name
				hitcheck.classification_name = classification_name
			hitcheck.name = get_joint_name(b_armature_basename, b_hitcheck)
			export_hitcheck(b_hitcheck, hitcheck, corrector, b_armature_basename)

		# rigid_body_list is present after PC
		if bone_info.context.version > 32:
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
	# support different constraint types
	for rd, b_joint, rbc in iter_constraints(joint_obs, joints, "ball", "POINT", j_map, b_armature_basename):
		pass
	for rd, b_joint, rbc in iter_constraints(joint_obs, joints, "hinge", "HINGE", j_map, b_armature_basename):
		rd.limits.min = rbc.limit_ang_z_lower
		rd.limits.max = rbc.limit_ang_z_upper
		# Z direction vec, not sure about the proper correction so a swizzle does the trick
		b_joint_mat = get_joint_matrix(b_joint)
		vec = b_joint_mat.to_3x3().col[2]
		rd.direction.set((-vec.x, vec.z, -vec.y))
	# print(joints.hinge_constraints)
	for rd, b_joint, rbc in iter_constraints(joint_obs, joints, "ragdoll", "GENERIC", j_map, b_armature_basename):
		# before correcting, rot tends to point y to the child joint
		# the z axis always matches that of the joint empty in blender
		b_joint_mat = get_joint_matrix(b_joint)
		b_joint_mat = b_joint_mat.to_3x3()
		cross = mathutils.Matrix(((0, 0, -1), (0, -1, 0), (-1, 0, 0)))
		b_joint_mat = b_joint_mat @ cross
		b_joint_mat = b_joint_mat.to_4x4()
		n_bind = corrector_rag.from_blender(b_joint_mat)
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
	for joint_i, b_joint in enumerate(joint_obs):
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


def get_armatures_collections(scene):
	armatures_collections = [(get_armature(mdl2_coll.objects), mdl2_coll) for mdl2_coll in scene.collection.children]
	# sort them so that armatures appear successively
	armatures_collections.sort(key=lambda tup: (str(tup[0]), tup[1].name))
	return armatures_collections
