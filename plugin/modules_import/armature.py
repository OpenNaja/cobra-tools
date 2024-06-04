import logging
import math

import bpy
import mathutils

import plugin.utils.transforms
from generated.formats.ms2.versions import is_ztuac, is_dla
from plugin.modules_import.collision import import_collider, parent_to

from plugin.utils.object import create_ob, set_collection_visibility, create_collection
from plugin.utils import blender_util
from plugin.utils.blender_util import vectorisclose
from plugin.utils.transforms import CorrectorRagdoll

TOLERANCE = 0.0001
vec_y = mathutils.Vector((0.0, 1.0, 0.0))


def import_armature(scene, model_info, b_bone_names, mdl2_coll):
	"""Scans an armature hierarchy, and returns a whole armature."""
	is_old_orientation = any((is_ztuac(model_info.context), is_dla(model_info.context)))
	# print(f"is_old_orientation {is_old_orientation}")
	corrector = plugin.utils.transforms.Corrector(is_old_orientation)
	# corrector = matrix_util.Corrector(False)
	bone_info = model_info.bone_info
	# logging.debug(bone_info)
	if bone_info:
		if bone_info.name in bpy.data.objects:
			armature_ob = bpy.data.objects[bone_info.name]
			return armature_ob
		b_armature_data = bpy.data.armatures.new(bone_info.name)
		b_armature_data.display_type = 'STICK'
		# b_armature_data.show_axes = True
		armature_ob = create_ob(scene, bone_info.name, b_armature_data, coll=mdl2_coll)
		armature_ob.show_in_front = True
		# make armature editable and create bones
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		z_dic = {}

		# flips = get_flips(b_bone_names, bone_info, corrector)
		long_name_2_short_name = {}
		mats = {}
		# JWE2 hoarding_straight8m_door has names that exceed the 63 char limit
		for i, (bone_name, bone, o_parent_ind) in enumerate(zip(b_bone_names, bone_info.bones, bone_info.parents)):
			b_edit_bone = b_armature_data.edit_bones.new(bone_name)
			b_edit_bone["long_name"] = bone_name
			long_name_2_short_name[bone_name] = b_edit_bone.name

			n_bind = get_local_bone_matrix(bone)
			# print(bone_name, n_bind)
			# link to parent
			try:
				if o_parent_ind not in (255, 65535):
					parent_long_name = b_bone_names[o_parent_ind]
					# needed to support long names
					parent_short_name = long_name_2_short_name[parent_long_name]
					b_edit_bone.parent = b_armature_data.edit_bones[parent_short_name]
					# calculate ms2 armature space matrix
					n_bind = mats[parent_short_name] @ n_bind
			except:
				logging.exception(f"Bone hierarchy error for bone {i} {bone_name} with parent index {o_parent_ind}")

			# store the ms2 armature space matrix
			mats[b_edit_bone.name] = n_bind
			# change orientation for blender bones
			b_bind = corrector.to_blender(n_bind)
			mat_3x3 = b_bind.to_3x3()
			# if bone_name in flips:
			# 	print(f"flipping {bone_name}")
			# 	# print(mat_3x3)
			# 	# mat_3x3 = flip_3x3_on_world_x_and_local_y(mat_3x3)
			# 	# flip = mathutils.Matrix().to_3x3()
			# 	# flip[0][0] = -1.0
			# 	# mat_3x3 = flip @ mat_3x3 @ flip
			# 	# works for JWE2 lips
			# 	flip_3x3_on_local_y(mat_3x3)
			# PZ penguin has roll that flips the rotation, but that's the way it is

			# set orientation to blender bone
			z_dic[b_edit_bone.name] = mat_3x3[2]
			tail, roll = bpy.types.Bone.AxisRollFromMatrix(mat_3x3)
			b_edit_bone.head = b_bind.to_translation()
			b_edit_bone.tail = tail + b_edit_bone.head
			b_edit_bone.roll = roll

		fix_bone_lengths(b_armature_data)
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

		# fix bone roll, gotta toggle modes once for the broken rolls to become apparent
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		for b_edit_bone in b_armature_data.edit_bones:
			# get the actual z axis from the matrix represented by this bone
			old_roll = math.degrees(b_edit_bone.roll)
			b_vec = b_edit_bone.matrix.to_3x3()[2]
			# form the angle between that and the desired bone bind's z axis
			a = b_vec.angle(z_dic[b_edit_bone.name])
			if a > TOLERANCE:
				# align it to original bone's z axis
				b_edit_bone.align_roll(z_dic[b_edit_bone.name])
				new_roll = math.degrees(b_edit_bone.roll)
				logging.debug(f"Changed broken bone roll for {b_edit_bone.name} ({old_roll:.1f}° -> {new_roll:.1f}°)")
		bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

		# store original bone index as custom property
		for i, bone_name in enumerate(b_bone_names):
			short_name = long_name_2_short_name[bone_name]
			bone = armature_ob.pose.bones[short_name]
			bone["index"] = i
		try:
			import_joints(scene, armature_ob, bone_info, b_bone_names, corrector, mdl2_coll)
		except:
			logging.exception("Importing joints failed")
		try:
			import_ik(scene, armature_ob, bone_info, b_bone_names, corrector, long_name_2_short_name)
		except:
			logging.exception("Importing IK failed")

		set_collection_visibility(scene, f"{model_info.name}_joints", True)
		set_collection_visibility(scene, f"{model_info.name}_hitchecks", True)
		return armature_ob


def set_transform(b_bind, b_edit_bone):
	tail, roll = bpy.types.Bone.AxisRollFromMatrix(b_bind.to_3x3())
	b_edit_bone.head = b_bind.to_translation()
	b_edit_bone.tail = tail + b_edit_bone.head
	b_edit_bone.roll = roll


def get_flips(b_bone_names, bone_info, corrector):
	mats1 = []
	for bone, o_parent_ind in zip(bone_info.bones, bone_info.parents):
		n_bind = get_local_bone_matrix(bone)
		# link to parent
		if o_parent_ind not in (255, 65535):
			# calculate ms2 armature space matrix
			n_bind = mats1[o_parent_ind].copy() @ n_bind
		# store the ms2 armature space matrix
		mats1.append(n_bind)
	mats_corrected = [corrector.to_blender(n_bind) for n_bind in mats1]
	vecs_map = {
		bone_name: (mat.to_3x3(), mat.to_translation()) for bone_name, mat in zip(b_bone_names, mats_corrected)
	}
	flips = set()
	for bone_name, (mat, loc) in vecs_map.items():
		# print(bone_name, loc)
		x_mirr = mathutils.Vector(loc)
		x_mirr.x *= -1.0
		# flip right channels, test that eg PZ pengu
		if loc.x < 0.0:
			# test for L R name first
			if bone_name.endswith(".R"):
				left_bone = bone_name[:-2] + ".L"
				other_mat, other_loc = vecs_map[left_bone]
				# print("mirror bone")
				if should_flip(mat, other_loc, other_mat, x_mirr):
					flips.add(bone_name)
			# no suffix, so check all bones
			else:
				for other_name, (other_mat, other_loc) in vecs_map.items():
					if should_flip(mat, other_loc, other_mat, x_mirr):
						flips.add(bone_name)
						break
	return flips


def flip_3x3_on_local_y(mat_3x3):
	mat_3x3[0][0] *= -1.0
	mat_3x3[0][1] *= -1.0
	mat_3x3[1][0] *= -1.0
	mat_3x3[1][1] *= -1.0
	mat_3x3[2][0] *= -1.0
	mat_3x3[2][1] *= -1.0


def should_flip(mat, other_loc, other_mat, x_mirr):
	if other_loc.x > 0.0:
		if vectorisclose(x_mirr, other_loc):
			print("close loc")
			# print(y_vec)
			# print(other_y_vec)
			# print(mat)
			# print(other_mat)
			# print(mat @ other_mat.inverted())
			# print(mat.inverted() @ other_mat)
			# print(mat @ other_mat)
			flipped = flip_3x3_on_world_x_and_local_y(mat)
			r_diff = flipped.to_quaternion().rotation_difference(other_mat.to_quaternion())
			if r_diff.angle < 0.01:
				print("flipping")
				return True
			flipped = flip_3x3_on_world_x_and_local_y_pz_pengu(mat)
			r_diff = flipped.to_quaternion().rotation_difference(other_mat.to_quaternion())
			if r_diff.angle < 0.01:
				print("flipping")
				return True
			# break


def flip_3x3_on_world_x_and_local_y(mat):
	m = mat.copy()
	m[0][0] *= -1.0
	m[0][2] *= -1.0
	m[1][1] *= -1.0
	m[2][1] *= -1.0
	return m


def flip_3x3_on_world_x_and_local_y_pz_pengu(mat):
	m = mat.copy()
	m[1] *= -1.0
	m[2] *= -1.0
	return m


def get_local_bone_matrix(bone):
	# local space matrix, in ms2 orientation
	n_bind = mathutils.Quaternion((bone.rot.w, bone.rot.x, bone.rot.y, bone.rot.z)).to_matrix().to_4x4()
	n_bind.translation = (bone.loc.x, bone.loc.y, bone.loc.z)
	return n_bind


def get_bone_names(model_info):
	if not model_info.bone_info:
		return []
	return [blender_util.bone_name_for_blender(bone.name) for bone in model_info.bone_info.bones]


def import_ik(scene, armature_ob, bone_info, b_bone_names, corrector, long_name_2_short_name):
	logging.info("Importing IK")
	ik = bone_info.ik_info
	# print(ik)

	def get_name(n):
		long_name = blender_util.bone_name_for_blender(n)
		short_name = long_name_2_short_name[long_name]
		return short_name

	child_2_parent = {}
	p_bones = armature_ob.pose.bones
	for ik_link in ik.ik_list:
		child_2_parent[ik_link.child.joint.name] = ik_link.parent.joint.name
		p_bone = p_bones[get_name(ik_link.child.joint.name)]
		p_bone.use_ik_limit_x = p_bone.use_ik_limit_y = p_bone.use_ik_limit_z = True
		p_bone.ik_min_x = -math.radians(ik_link.yaw.min)
		p_bone.ik_max_x = math.radians(ik_link.yaw.max)
		p_bone.ik_min_y = p_bone.ik_max_y = 0.0
		p_bone.ik_min_z = -math.radians(ik_link.pitch.min)
		p_bone.ik_max_z = math.radians(ik_link.pitch.max)

		# debug ik matrix
		# b_ik = create_ob(scene, f"{'ik'}_{ik_link.child.joint.name}", None, coll_name="ik")
		# b_ik.empty_display_type = "ARROWS"
		# b_ik.empty_display_size = 0.05
		# # mat = mathutils.Matrix(ik_link.matrix.data).inverted().to_4x4()
		# mat = mathutils.Matrix(ik_link.matrix.data).to_4x4()
		# # mat = corrector.to_blender(mat)
		# # mat = get_matrix(corrector, ik_link.matrix)
		# # mat = mat.to_3x3()
		# # cross = mathutils.Matrix(((0, 0, -1), (0, -1, 0), (-1, 0, 0)))
		# # mat = mat @ cross
		# mat = mat.to_4x4()
		# p_bone = armature_ob.pose.bones[matrix_util.bone_name_for_blender(ik_link.child.joint.name)]
		# loc = p_bone.bone.matrix_local.translation
		# mat.translation = loc
		# b_ik.matrix_local = mat
		# print(ik_link)
	# find ends of chains
	chains = {}
	for child, parent in child_2_parent.items():
		if child not in child_2_parent.values():
			chains[child] = []
	# complete the chains
	for child, parents in chains.items():
		while True:
			parent = child_2_parent.get(child, None)
			if parent:
				parents.append(parent)
				child = parent
			else:
				break

	# create a copy location constraint for each ik target
	for ik_target in ik.ik_targets:
		end_name = ik_target.ik_end.joint.name
		target_name = ik_target.ik_blend.joint.name
		# copy rot of the IK controller
		p_bone = armature_ob.pose.bones[get_name(end_name)]
		b_copy = p_bone.constraints.new("COPY_ROTATION")
		b_copy.target = armature_ob
		b_copy.subtarget = get_name(target_name)
		if end_name in chains:
			chain = chains.pop(end_name)
			# add an ik constraint to the end
			if len(chain) > 1:
				b_ik = p_bone.constraints.new("IK")
				b_ik.chain_count = len(chain)
				b_ik.target = armature_ob
				b_ik.use_tail = False
				b_ik.subtarget = get_name(target_name)
			else:
				raise AttributeError(f"IK chain too short")

	# create the bare constraints
	for child, parents in chains.items():
		p_bone = armature_ob.pose.bones[get_name(child)]
		b_ik = p_bone.constraints.new("IK")
		b_ik.chain_count = len(parents)


def import_joints(scene, armature_ob, bone_info, b_bone_names, corrector, mdl2_coll):
	logging.info("Importing joints")
	j = bone_info.joints
	joint_map = {}
	if bone_info.joint_count:
		joint_coll = create_collection(f"{mdl2_coll.name}_joints", mdl2_coll)
	# if joint_info.hitchecks:
	# 	joint_coll = create_collection(f"{mdl2_coll.name}_joints", mdl2_coll)
	for joint_i, (bone_index, joint_info, joint_transform) in enumerate(zip(
			j.joint_to_bone, j.joint_infos, j.joint_transforms)):
		logging.debug(f"joint {joint_info.name}")
		# create an empty representing the joint
		b_joint = create_ob(scene, f"{mdl2_coll.name}_{joint_info.name}", None, coll=joint_coll)
		b_joint["long_name"] = joint_info.name
		joint_map[joint_info.name] = b_joint
		b_joint.empty_display_type = "ARROWS"
		b_joint.empty_display_size = 0.05
		# this is in armature space, parenting later will make it relative to the bone
		b_joint.matrix_local = get_matrix(corrector, joint_transform.rot, joint_transform.loc)

		if hasattr(joint_info, "hitchecks"):
			for hitcheck in joint_info.hitchecks:
				b_collider = import_collider(hitcheck, b_joint, corrector, joint_coll)
				# not used by PC
				if j.rigid_body_list:
					rb = j.rigid_body_list[joint_i]
					b_collider.rigid_body.mass = rb.mass
					b_collider.cobra_coll.air_resistance[0] = rb.air_resistance_x
					b_collider.cobra_coll.air_resistance[1] = rb.air_resistance_y
					b_collider.cobra_coll.air_resistance[2] = rb.air_resistance_z
					b_collider.cobra_coll.damping_3d[0] = rb.unk_1
					b_collider.cobra_coll.damping_3d[1] = rb.unk_2
					b_collider.cobra_coll.damping_3d[2] = rb.unk_4
					b_collider.cobra_coll.flag = rb.flag.name
					# when type = 0, unks are 0.0 and frictions are all the same
		# attach joint to bone
		bone_name = b_bone_names[bone_index]
		parent_to(armature_ob, b_joint, bone_name)

	corrector_rag = CorrectorRagdoll(False)
	# ragdoll constraints
	for ragdoll in j.ragdoll_constraints:
		b_joint, rbc = add_rb_constraint(joint_map, ragdoll, constraint_type="GENERIC")
		rbc.use_limit_ang_x = rbc.use_limit_ang_y = rbc.use_limit_ang_z = True
		rbc.limit_ang_x_lower = -ragdoll.x.min
		rbc.limit_ang_x_upper = ragdoll.x.max
		rbc.limit_ang_y_lower = -ragdoll.y.min
		rbc.limit_ang_y_upper = ragdoll.y.max
		rbc.limit_ang_z_lower = -ragdoll.z.min
		rbc.limit_ang_z_upper = ragdoll.z.max
		rbc.use_limit_lin_x = rbc.use_limit_lin_y = rbc.use_limit_lin_z = True
		rbc.limit_lin_x_lower = rbc.limit_lin_x_upper = rbc.limit_lin_y_lower = rbc.limit_lin_y_upper = \
			rbc.limit_lin_z_lower = rbc.limit_lin_z_upper = 0.0
		# plasticity
		b_joint.cobra_coll.plasticity_min = ragdoll.plasticity.min
		b_joint.cobra_coll.plasticity_max = ragdoll.plasticity.max

		# # debug ragdoll matrix
		# b_ragdoll = create_ob(scene, f"{'ragdoll'}_{child_name}", None, coll_name="ragdoll")
		# b_ragdoll.empty_display_type = "ARROWS"
		# b_ragdoll.empty_display_size = 0.05
		# mat = get_matrix(corrector_rag, ragdoll.rot)
		# mat = mat.to_3x3()
		# cross = mathutils.Matrix(((0, 0, -1), (0, -1, 0), (-1, 0, 0)))
		# mat = mat @ cross
		# mat = mat.to_4x4()
		# joint_transform = j.joint_transforms[ragdoll.child.index]
		# mat.translation = get_matrix(corrector, joint_transform.rot, joint_transform.loc).translation
		# b_ragdoll.matrix_local = mat
		#
		# # debug ragdoll vec_b
		# b_trg = create_ob(scene, f"{'target'}_{child_name}", None, coll_name="target")
		# b_trg.empty_display_type = "PLAIN_AXES"
		# b_trg.empty_display_size = 0.05
		# mat2 = mathutils.Matrix().to_4x4()
		# # unsure if that transform is correct
		# n_bind = mathutils.Matrix().to_4x4()
		# n_bind.translation = (ragdoll.vec_b.x, ragdoll.vec_b.y, ragdoll.vec_b.z)
		# b_bind = corrector_rag.to_blender(n_bind)
		# mat2.translation = mat.translation - (mathutils.Vector(ragdoll.vec_b) * 0.1)
		# # mat2.translation = mat.translation + (mathutils.Vector(b_bind.translation) * 0.1)
		# b_trg.matrix_local = mat2
		# # print(ragdoll)

	for ball in j.ball_constraints:
		b_joint, rbc = add_rb_constraint(joint_map, ball, constraint_type="POINT")
		# tr = j.joint_transforms[ball.child.index]

	for hinge in j.hinge_constraints:
		# print(hinge)
		b_joint, rbc = add_rb_constraint(joint_map, hinge, constraint_type="HINGE")
		rbc.use_limit_ang_z = True
		rbc.limit_ang_z_lower = hinge.limits.min
		rbc.limit_ang_z_upper = hinge.limits.max
		# # debug hinge direction
		# b_trg = create_ob(scene, f"{'target'}_{b_joint.name}", None, coll_name="target")
		# b_trg.empty_display_type = "PLAIN_AXES"
		# b_trg.empty_display_size = 0.05
		# n_bind = mathutils.Matrix().to_4x4()
		# n_bind.translation = (hinge.direction.x, hinge.direction.y, hinge.direction.z)
		# b_bind = corrector_rag.to_blender(n_bind)
		# mat2 = mathutils.Matrix().to_4x4()
		# mat2.translation = b_joint.matrix_world.translation + (mathutils.Vector(b_bind.translation) * 0.1)
		# b_trg.matrix_world = mat2


def add_rb_constraint(joint_map, constraint, constraint_type="GENERIC"):
	parent_name = constraint.parent.joint.name
	child_name = constraint.child.joint.name
	b_joint = joint_map[child_name]
	# override = bpy.context.copy()
	# override['selected_objects'] = b_joint
	# override['active_object'] = b_joint
	# bpy.ops.rigidbody.object_add(override)
	bpy.context.view_layer.objects.active = b_joint
	bpy.ops.rigidbody.constraint_add()
	rbc = b_joint.rigid_body_constraint
	rbc.type = constraint_type
	child_collider = joint_map[child_name].children[0]
	parent_collider = joint_map[parent_name].children[0]
	rbc.object1 = child_collider
	rbc.object2 = parent_collider
	# only set constrained children to active
	child_collider.rigid_body.type = "ACTIVE"
	# print(constraint.parent.joint)
	# print(constraint.child.joint)
	return b_joint, rbc


def get_matrix(corrector, rot_mat, vec=None):
	n_bind = mathutils.Matrix(rot_mat.data).inverted().to_4x4()
	if vec is not None:
		n_bind.translation = (vec.x, vec.y, vec.z)
	b_bind = corrector.to_blender(n_bind)
	return b_bind


def fix_bone_lengths(b_armature_data):
	"""Sets all edit_bones to a suitable length."""
	for b_edit_bone in b_armature_data.edit_bones:
		# don't change root bones
		if b_edit_bone.parent:
			# calculate length based on position of children
			if b_edit_bone.children:
				children = [(len(b_child.children), b_child) for b_child in b_edit_bone.children]
				# can't sort bones, so just sort counts
				children.sort(key=lambda tup: tup[0], reverse=True)
				# check if there is a bone that has more (recursive) children than the others
				# if so, use that one to get the length
				if len(children) > 1 and children[0][0] > children[1][0]:
					bone_length = (b_edit_bone.head - children[0][1].head).length
				else:
					# average position of all children's heads
					child_heads = mathutils.Vector()
					for b_child in b_edit_bone.children:
						child_heads += b_child.head
					bone_length = (b_edit_bone.head - child_heads / len(b_edit_bone.children)).length
			# end of a chain
			else:
				if (b_edit_bone.parent.tail - b_edit_bone.head).length < TOLERANCE:
					# continues a chain from the parent
					bone_length = b_edit_bone.parent.length
				else:
					# it is isolated from the parent, so make the bone smaller to uncluster the rig
					bone_length = b_edit_bone.parent.length * 0.3
		else:
			bone_length = b_edit_bone.length
		# clamp to a safe minimum length
		if bone_length < TOLERANCE:
			bone_length = 0.1
		b_edit_bone.length = bone_length


def append_armature_modifier(b_obj, b_armature):
	"""Append an armature modifier for the object."""
	if b_obj and b_armature:
		b_obj.parent = b_armature
		b_mod = b_obj.modifiers.new(b_armature.name, 'ARMATURE')
		b_mod.object = b_armature
		b_mod.use_bone_envelopes = False
		b_mod.use_vertex_groups = True


def resolve_name(b_bone_names, bone_index):
	try:
		# already converted to blender convention
		return b_bone_names[bone_index]
	except:
		return str(bone_index)


def import_vertex_groups(ob, mesh, b_bone_names):
	logging.debug(f"Importing vertex groups for {ob.name}...")
	# sort by bone name
	for bone_index in sorted(mesh.weights_info.keys(), key=lambda x: resolve_name(b_bone_names, x)):
		weights_dic = mesh.weights_info[bone_index]
		bonename = resolve_name(b_bone_names, bone_index)
		ob.vertex_groups.new(name=bonename)
		for weight, vert_indices in weights_dic.items():
			ob.vertex_groups[bonename].add(vert_indices, weight, 'REPLACE')
