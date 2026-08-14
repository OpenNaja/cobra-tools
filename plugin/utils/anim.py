import math

import bpy
import mathutils


def get_bone_bind_data(b_armature_ob : bpy.types.Object, bones_table, corrector) -> tuple[list[mathutils.Matrix], list[mathutils.Matrix]]:
	"""Returns a list of bind matrices in game's armature space according to corrector and
	a list of local matrices in blender's local space (relative to the parent bone)."""
	g_bind_matrices = []
	b_local_matrices = []
	for bone_i, bone_name in bones_table:
		if bone_name in b_armature_ob.data.bones:
			b_bone = b_armature_ob.data.bones[bone_name]
			b_bind = b_bone.matrix_local
			b_local = mathutils.Matrix(b_bind)
			if b_bone.parent:
				b_local = b_bone.parent.matrix_local.inverted() @ b_local
			b_local_matrices.append(b_local)
			g_bind_matrices.append(corrector.from_blender(b_bind))
		else:
			b_local_matrices.append(mathutils.Matrix().to_4x4())
			g_bind_matrices.append(mathutils.Matrix().to_4x4())
	return g_bind_matrices, b_local_matrices


c_map = (
	("Footplant", "FLOOR", True, None),
	("BlendHeadLookOut", "TRACK_TO", True, None),
	# range +-pi, looped locomotion anims lerp from -pi to +pi, apparently denotes the phase of the limbs, stand is 0
	("phaseStream", "LOCKED_TRACK", True, (-math.pi, math.pi)),
	("IKEnabled", "IK", False, None)
)