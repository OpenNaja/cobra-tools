import mathutils


def get_bone_bind_data(b_armature_ob, bones_table, corrector):
	binds = []
	bones_local_mat = []
	for bone_i, bone_name in bones_table:
		b_bone = b_armature_ob.data.bones[bone_name]
		b_bind = b_bone.matrix_local
		b_local = mathutils.Matrix(b_bind)
		if b_bone.parent:
			b_local = b_bone.parent.matrix_local.inverted() @ b_local
		bones_local_mat.append(b_local)
		bind = corrector.blender_bind_to_nif_bind(b_bind)
		# inv_bind = bind.inverted()
		# bind_loc = b_armature_ob.data.bones[bone_name].matrix_local.translation
		# bind_loc_inv = bind_loc.negate()
		binds.append(bind)
	return binds, bones_local_mat
