import logging
import math

import bpy
import mathutils

from generated.formats.ms2.versions import is_ztuac, is_dla
from plugin.modules_import.collision import import_collider, parent_to

from plugin.utils.object import create_ob, link_to_collection, set_collection_visibility
from plugin.utils import matrix_util
from plugin.utils.matrix_util import mat3_to_vec_roll, CorrectorRagdoll


def import_armature(scene, model_info, b_bone_names):
	"""Scans an armature hierarchy, and returns a whole armature."""
	is_old_orientation = any((is_ztuac(model_info.context), is_dla(model_info.context)))
	# print(f"is_old_orientation {is_old_orientation}")
	corrector = matrix_util.Corrector(is_old_orientation)
	bone_info = model_info.bone_info
	# logging.debug(bone_info)
	if bone_info:
		armature_name = f"{scene.name}_armature"
		b_armature_data = bpy.data.armatures.new(armature_name)
		b_armature_data.display_type = 'STICK'
		# b_armature_data.show_axes = True
		armature_ob = create_ob(scene, armature_name, b_armature_data)
		armature_ob.show_in_front = True
		# make armature editable and create bones
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		mats = {}
		z_dic = {}
		long_name_2_short_name = {}
		# JWE2 hoarding_straight8m_door has names that exceed the 63 char limit
		for bone_name, bone, o_parent_ind in zip(b_bone_names, bone_info.bones, bone_info.parents):
			b_edit_bone = b_armature_data.edit_bones.new(bone_name)
			b_edit_bone["long_name"] = bone_name
			long_name_2_short_name[bone_name] = b_edit_bone.name

			n_bind = get_local_bone_matrix(bone)

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
				logging.exception(f"Bone hierarchy error for bone {bone_name} with parent index {o_parent_ind}")

			# store the ms2 armature space matrix
			mats[b_edit_bone.name] = n_bind
			# change orientation for blender bones
			b_bind = corrector.nif_bind_to_blender_bind(n_bind)
			z_dic[b_edit_bone.name] = b_bind.to_3x3()[2]
			# set orientation to blender bone
			set_transform4(b_bind, b_edit_bone)

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
			if a > 0.0001:
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
			import_joints(scene, armature_ob, bone_info, b_bone_names, corrector)
		except:
			logging.exception("Importing joints failed")
		try:
			import_ik(scene, armature_ob, bone_info, b_bone_names, corrector, long_name_2_short_name)
		except:
			logging.exception("Importing IK failed")

		set_collection_visibility(scene, f"{scene.name}_joints", True)
		set_collection_visibility(scene, f"{scene.name}_hitchecks", True)
		return armature_ob


def get_local_bone_matrix(bone):
	# local space matrix, in ms2 orientation
	n_bind = mathutils.Quaternion((bone.rot.w, bone.rot.x, bone.rot.y, bone.rot.z)).to_matrix().to_4x4()
	n_bind.translation = (bone.loc.x, bone.loc.y, bone.loc.z)
	return n_bind


def set_transform1(b_bind, b_edit_bone):
	# now simplified to handle tail = -Y
	tail, roll = mat3_to_vec_roll(b_bind.to_3x3())
	b_edit_bone.head = b_bind.to_translation()
	b_edit_bone.tail = tail + b_edit_bone.head
	b_edit_bone.roll = roll


def set_transform2(b_bind, b_edit_bone):
	# identical to 4
	b_edit_bone.head = (0, 0, 0)
	b_edit_bone.tail = (-1, 0, 0)
	b_edit_bone.matrix = b_bind


def set_transform3(b_bind, b_edit_bone):
	b_edit_bone.tail = (0, 1, 0)
	# seemingly no matter what roll is set to, it's not correct
	b_edit_bone.roll = math.radians(180)
	b_edit_bone.transform(b_bind, roll=True)


def set_transform4(b_bind, b_edit_bone):
	# identical to 2
	tail, roll = bpy.types.Bone.AxisRollFromMatrix(b_bind.to_3x3())
	b_edit_bone.head = b_bind.to_translation()
	b_edit_bone.tail = tail + b_edit_bone.head
	b_edit_bone.roll = roll


def get_bone_names(model_info):
	if not model_info.bone_info:
		return []
	return [matrix_util.bone_name_for_blender(bone.name) for bone in model_info.bone_info.bones]


def import_ik(scene, armature_ob, bone_info, b_bone_names, corrector, long_name_2_short_name):
	logging.info("Importing IK")
	ik = bone_info.ik_info
	child_2_parent = {}
	for ik_link in ik.ik_list:
		child_2_parent[ik_link.child.joint.name] = ik_link.parent.joint.name
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
	# create the constraints
	for child, parents in chains.items():
		b_long_name = matrix_util.bone_name_for_blender(child)
		b_short_name = long_name_2_short_name[b_long_name]
		p_bone = armature_ob.pose.bones[b_short_name]
		b_ik = p_bone.constraints.new("IK")
		b_ik.chain_count = len(parents) + 1


def import_joints(scene, armature_ob, bone_info, b_bone_names, corrector):
	logging.info("Importing joints")
	j = bone_info.joints
	joint_map = {}
	for joint_i, (bone_index, joint_info, joint_transform) in enumerate(zip(
			j.joint_to_bone, j.joint_infos, j.joint_transforms)):
		logging.debug(f"joint {joint_info.name}")
		# create an empty representing the joint
		b_joint = create_ob(scene, f"{bpy.context.scene.name}_{joint_info.name}", None, coll_name="joints")
		b_joint["long_name"] = joint_info.name
		joint_map[joint_info.name] = b_joint
		b_joint.empty_display_type = "ARROWS"
		b_joint.empty_display_size = 0.05
		# this is in armature space, parenting later will make it relative to the bone
		b_joint.matrix_local = get_matrix(corrector, joint_transform.rot, joint_transform.loc)

		if hasattr(joint_info, "hitchecks"):
			for hitcheck in joint_info.hitchecks:
				b_collider = import_collider(hitcheck, b_joint, corrector)
				# not used by PC
				if j.rigid_body_list:
					rb = j.rigid_body_list[joint_i]
					b_collider.rigid_body.mass = rb.mass
		# attach joint to bone
		bone_name = b_bone_names[bone_index]
		parent_to(armature_ob, b_joint, bone_name)

	corrector_rag = CorrectorRagdoll(False)
	# ragdoll constraints
	for ragdoll in j.ragdoll_constraints:
		parent_name = ragdoll.parent.joint.name
		child_name = ragdoll.child.joint.name
		b_joint = joint_map[child_name]
		# override = bpy.context.copy()
		# override['selected_objects'] = b_joint
		# override['active_object'] = b_joint
		# bpy.ops.rigidbody.object_add(override)
		bpy.context.view_layer.objects.active = b_joint
		bpy.ops.rigidbody.constraint_add()
		rbc = b_joint.rigid_body_constraint
		rbc.type = 'GENERIC'
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
		ob1 = joint_map[child_name].children[0]
		ob2 = joint_map[parent_name].children[0]
		rbc.object1 = ob1
		rbc.object2 = ob2
		# only set constrained children to active
		ob1.rigid_body.type = "ACTIVE"

		b_ragdoll = create_ob(scene, f"{'ragdoll'}_{child_name}", None, coll_name="ragdoll")
		b_ragdoll.empty_display_type = "ARROWS"
		b_ragdoll.empty_display_size = 0.05
		mat = get_matrix(corrector_rag, ragdoll.rot)
		mat = mat.to_3x3()
		cross = mathutils.Matrix(((0, 0, -1), (0, -1, 0), (-1, 0, 0)))
		mat = mat @ cross
		mat = mat.to_4x4()
		joint_transform = j.joint_transforms[ragdoll.child.index]
		mat.translation = get_matrix(corrector, joint_transform.rot, joint_transform.loc).translation
		b_ragdoll.matrix_local = mat

		b_trg = create_ob(scene, f"{'target'}_{child_name}", None, coll_name="target")
		b_trg.empty_display_type = "PLAIN_AXES"
		b_trg.empty_display_size = 0.05
		mat2 = mathutils.Matrix().to_4x4()
		# unsure if that transform is correct
		n_bind = mathutils.Matrix().to_4x4()
		n_bind.translation = (ragdoll.vec_b.x, ragdoll.vec_b.y, ragdoll.vec_b.z)
		b_bind = corrector_rag.nif_bind_to_blender_bind(n_bind)
		mat2.translation = mat.translation - (mathutils.Vector(ragdoll.vec_b) * 0.1)
		# mat2.translation = mat.translation + (mathutils.Vector(b_bind.translation) * 0.1)
		b_trg.matrix_local = mat2
		# print(ragdoll)


def get_matrix(corrector, rot_mat, vec=None):
	n_bind = mathutils.Matrix(rot_mat.data).inverted().to_4x4()
	if vec is not None:
		n_bind.translation = (vec.x, vec.y, vec.z)
	b_bind = corrector.nif_bind_to_blender_bind(n_bind)
	return b_bind


def fix_bone_lengths(b_armature_data):
	"""Sets all edit_bones to a suitable length."""
	for b_edit_bone in b_armature_data.edit_bones:
		# don't change root bones
		if b_edit_bone.parent:
			# take the desired length from the mean of all children's heads
			if b_edit_bone.children:
				# trying to get closer to the actual, most relevant child
				# lengths = [(b_edit_bone.head-b_child.head).length for b_child in b_edit_bone.children]
				# dists = [(b_edit_bone.head + (b_edit_bone.tail - b_edit_bone.head) * l - b_child.head).length for l, b_child in zip(lengths, b_edit_bone.children)]
				# # print(b_edit_bone.name, lengths, dists)
				# nonzero_dists = [(val, idx) for (idx, val) in enumerate(dists) if val > 0.0]
				# if nonzero_dists:
				# 	val, idx = min(nonzero_dists)
				# 	bone_length = lengths[idx]
				# else:
				child_heads = mathutils.Vector()
				for b_child in b_edit_bone.children:
					child_heads += b_child.head
				bone_length = (b_edit_bone.head - child_heads / len(b_edit_bone.children)).length
			# end of a chain
			else:
				bone_length = b_edit_bone.parent.length
		else:
			bone_length = b_edit_bone.length
		# clamp to a safe minimum length
		if bone_length < 0.0001:
			bone_length = 0.1
		b_edit_bone.length = bone_length


def append_armature_modifier(b_obj, b_armature):
	"""Append an armature modifier for the object."""
	if b_obj and b_armature:
		b_obj.parent = b_armature
		armature_name = b_armature.name
		b_mod = b_obj.modifiers.new(armature_name, 'ARMATURE')
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
