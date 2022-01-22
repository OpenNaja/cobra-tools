import logging
import math
import traceback

import bpy
import mathutils

from generated.formats.ms2.versions import is_ztuac
from plugin.modules_import.collision import import_collider

from plugin.helpers import create_ob
from plugin.utils import matrix_util
from plugin.utils.matrix_util import mat3_to_vec_roll


def import_armature(mdl2, b_bone_names):
	"""Scans an armature hierarchy, and returns a whole armature.
	This is done outside the normal node tree scan to allow for positioning
	of the bones before skins are attached."""
	corrector = matrix_util.Corrector(is_ztuac(mdl2))
	bone_info = mdl2.bone_info
	print(bone_info)
	if bone_info:
		armature_name = b_bone_names[0]
		b_armature_data = bpy.data.armatures.new(armature_name)
		b_armature_data.display_type = 'STICK'
		# b_armature_data.show_axes = True
		# set axis orientation for export
		# b_armature_data.niftools.axis_forward = NifOp.props.axis_forward
		# b_armature_data.niftools.axis_up = NifOp.props.axis_up
		b_armature_obj = create_ob(armature_name, b_armature_data)
		b_armature_obj.show_in_front = True
		# make armature editable and create bones
		bpy.ops.object.mode_set(mode='EDIT', toggle=False)
		mats = {}
		z_dic = {}
		for bone_name, bone, o_parent_ind in zip(b_bone_names, bone_info.bones, bone_info.parents):
			b_edit_bone = b_armature_data.edit_bones.new(bone_name)

			n_bind = get_local_bone_matrix(bone)

			# link to parent
			try:
				if o_parent_ind != 255:
					parent_name = b_bone_names[o_parent_ind]
					b_parent_bone = b_armature_data.edit_bones[parent_name]
					b_edit_bone.parent = b_parent_bone
					# calculate ms2 armature space matrix
					n_bind = mats[parent_name] @ n_bind
			except:
				logging.warning(f"Bone hierarchy error for bone {bone_name} with parent index {o_parent_ind}")

			# store the ms2 armature space matrix
			mats[bone_name] = n_bind
			# change orientation for blender bones
			b_bind = corrector.nif_bind_to_blender_bind(n_bind)
			z_dic[bone_name] = b_bind.to_3x3()[2]
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
			bone = b_armature_obj.pose.bones[bone_name]
			bone["index"] = i
		try:
			import_joints(b_armature_obj, bone_info, b_bone_names, corrector)
		except Exception as err:
			print("Importing joints failed...", err)
			traceback.print_exc()
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


def get_bone_names(mdl2):
	if not mdl2.bone_info:
		return []
	return [matrix_util.bone_name_for_blender(bone.name) for bone in mdl2.bone_info.bones]


def import_joints(armature_ob, bone_info, b_bone_names, corrector):
	print("Importing joints")
	for bone_index, joint_info in zip(bone_info.joints.joint_indices, bone_info.joints.joint_infos):
		bone_name = b_bone_names[bone_index]
		print("joint", joint_info.name)
		if hasattr(joint_info, "hitchecks"):
			for hitcheck in joint_info.hitchecks:
				import_collider(hitcheck, armature_ob, bone_name, corrector)
	# for bone_index, hitcheck in zip(bone_info.joints.joint_indices, bone_info.joints.hitchecks_pc):
	# 	bone_name = b_bone_names[bone_index]
	# 	import_collider(hitcheck, armature_ob, bone_name, corrector)
	for bone_index, joint_transform in zip(bone_info.joints.joint_indices, bone_info.joints.joint_transforms):
		bone_name = b_bone_names[bone_index]
		joint = create_ob("joint_"+bone_name, None)
		n_bind = mathutils.Matrix(joint_transform.rot.data).inverted().to_4x4()
		n_bind.translation = (joint_transform.loc.x, joint_transform.loc.y, joint_transform.loc.z)
		b_bind = corrector.nif_bind_to_blender_bind(n_bind)
		joint.empty_display_type = "ARROWS"
		joint.empty_display_size = 0.03
		joint.matrix_local = b_bind
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
	# 		joint = create_ob("struct7_"+bone_name_0, None)
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
				child_heads = mathutils.Vector()
				for b_child in b_edit_bone.children:
					child_heads += b_child.head
				bone_length = (b_edit_bone.head - child_heads / len(b_edit_bone.children)).length
				if bone_length < 0.0001:
					bone_length = 0.1
			# end of a chain
			else:
				bone_length = b_edit_bone.parent.length
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


def get_weights(model):
	dic = {}
	for i, vert in enumerate(model.weights):
		for bone_index, weight in vert:
			if bone_index not in dic:
				dic[bone_index] = {}
			if weight not in dic[bone_index]:
				dic[bone_index][weight] = []
			dic[bone_index][weight].append(i)
	return dic


def resolve_name(b_bone_names, bone_index):
	try:
		# already converted to blender convention
		return b_bone_names[bone_index]
	except:
		return str(bone_index)


def import_vertex_groups(ob, model, b_bone_names):
	logging.debug(f"Importing vertex groups for {ob.name}...")
	# sort by bone name
	for bone_index in sorted(model.weights_info.keys(), key=lambda x: resolve_name(b_bone_names, x)):
		weights_dic = model.weights_info[bone_index]
		bonename = resolve_name(b_bone_names, bone_index)
		ob.vertex_groups.new(name=bonename)
		for weight, vert_indices in weights_dic.items():
			ob.vertex_groups[bonename].add(vert_indices, weight/255, 'REPLACE')
