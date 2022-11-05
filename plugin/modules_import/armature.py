import logging
import math

import bpy
import mathutils

from generated.formats.ms2.versions import is_ztuac, is_dla
from plugin.modules_import.collision import import_collider, parent_to

from plugin.utils.object import create_ob, link_to_collection
from plugin.utils import matrix_util
from plugin.utils.matrix_util import mat3_to_vec_roll


def import_armature(scene, model_info, b_bone_names):
	"""Scans an armature hierarchy, and returns a whole armature.
	This is done outside the normal node tree scan to allow for positioning
	of the bones before skins are attached."""
	is_old_orientation = any((is_ztuac(model_info.context), is_dla(model_info.context)))
	# print(f"is_old_orientation {is_old_orientation}")
	corrector = matrix_util.Corrector(is_old_orientation)
	bone_info = model_info.bone_info
	# logging.debug(bone_info)
	if bone_info:
		armature_name = f"{scene.name}_armature"
		b_armature_data = bpy.data.armatures.new(armature_name)
		b_armature_data.display_type = 'STICK'
		b_armature_data.show_axes = True
		# set axis orientation for export
		# b_armature_data.niftools.axis_forward = NifOp.props.axis_forward
		# b_armature_data.niftools.axis_up = NifOp.props.axis_up
		b_armature_obj = create_ob(scene, armature_name, b_armature_data)
		b_armature_obj.show_in_front = True
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
				if o_parent_ind != 255:
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
			bone = b_armature_obj.pose.bones[short_name]
			bone["index"] = i
		try:
			import_joints(scene, b_armature_obj, bone_info, b_bone_names, corrector)
		except:
			logging.exception("Importing joints failed...")
		return b_armature_obj


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


def import_joints(scene, armature_ob, bone_info, b_bone_names, corrector):
	logging.info("Importing joints")
	j = bone_info.joints
	for bone_index, joint_info, joint_transform in zip(j.joint_indices, j.joint_infos, j.joint_transforms):
		logging.debug(f"joint {joint_info.name}")
		# create an empty representing the joint
		b_joint = create_ob(scene, f"{bpy.context.scene.name}_{joint_info.name}", None, coll_name="joints")
		b_joint["long_name"] = joint_info.name
		b_joint.empty_display_type = "ARROWS"
		b_joint.empty_display_size = 0.03
		b_joint.matrix_local = get_matrix(corrector, joint_transform)
		if hasattr(joint_info, "hitchecks"):
			for hitcheck in joint_info.hitchecks:
				import_collider(hitcheck, b_joint, corrector)
		# attach joint to bone
		bone_name = b_bone_names[bone_index]
		parent_to(armature_ob, b_joint, bone_name)


def get_matrix(corrector, joint_transform):
	n_bind = mathutils.Matrix(joint_transform.rot.data).inverted().to_4x4()
	n_bind.translation = (joint_transform.loc.x, joint_transform.loc.y, joint_transform.loc.z)
	b_bind = corrector.nif_bind_to_blender_bind(n_bind)
	return b_bind


# try:
	# 	for item in bone_info.struct_7.unknown_list:
	# 		bone_name_0 = b_bone_names[item.parent]
	# 		bone_name_1 = b_bone_names[item.child]
	# 		print("struct7", bone_name_0, bone_name_1)
	# 		# print("struct7", item.vector)
	# 		print(mathutils.Matrix(item.matrix.data))
	# 		b0 = bone_info.bones[item.parent]
	# 		b1 = bone_info.bones[item.child]
	# 		m0 = get_local_bone_matrix(b0).to_3x3()
	# 		m1 = get_local_bone_matrix(b1).to_3x3()
	# 		# print(m0)
	# 		# print(m1)
	# 		# print(m0.inverted())
	# 		# print(m1.inverted())
	# 		print(m0 @ m1)
	# 		print((m0 @ m1).inverted())
	# 		it0 = bone_info.inverse_bind_matrices[item.parent]
	# 		it1 = bone_info.inverse_bind_matrices[item.child]
	# 		i0 = mathutils.Matrix(it0.data).inverted()
	# 		i1 = mathutils.Matrix(it1.data).inverted()
	# 		print(i0)
	# 		print(i1)
	# 		joint = create_ob(scene, "struct7_"+bone_name_0, None)
	# 		n_bind = mathutils.Matrix(item.matrix.data).inverted().to_4x4()
	# 		# n_bind.translation = (item.vector.x, item.vector.y, item.vector.z)
	# 		b_bind = corrector.nif_bind_to_blender_bind(n_bind)
	# 		joint.empty_display_type = "ARROWS"
	# 		joint.empty_display_size = 0.03
	# 		joint.matrix_local = b_bind
	# except:
	# 	pass


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
