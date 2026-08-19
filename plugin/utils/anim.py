import math
import logging

import bpy
import mathutils


def get_bone_bind_data(b_armature_ob : bpy.types.Object, bones_table, corrector) -> tuple[list[mathutils.Matrix], list[mathutils.Matrix]]:
	"""Returns a list of bind matrices in game's armature space according to corrector and
	a list of local matrices in blender's local space (relative to the parent bone)."""
	g_bind_armature_space = []
	b_bind_local_space = []
	for bone_i, bone_name in bones_table:
		if bone_name in b_armature_ob.data.bones:
			b_bone = b_armature_ob.data.bones[bone_name]
			b_bind_local_space.append(get_b_local_matrix(b_bone))
			g_bind_armature_space.append(corrector.from_blender(b_bone.matrix_local))
		else:
			b_bind_local_space.append(mathutils.Matrix().to_4x4())
			g_bind_armature_space.append(mathutils.Matrix().to_4x4())
	return g_bind_armature_space, b_bind_local_space


c_map = (
	("Footplant", "FLOOR", True, None),
	("BlendHeadLookOut", "TRACK_TO", True, None),
	# range +-pi, looped locomotion anims lerp from -pi to +pi, apparently denotes the phase of the limbs, stand is 0
	("phaseStream", "LOCKED_TRACK", True, (-math.pi, math.pi)),
	("IKEnabled", "IK", False, None)
)


def get_b_local_matrix(b_bone: bpy.types.Bone) -> mathutils.Matrix:
	"""Returns the local space matrix for b_bone in blender coordinates."""
	if b_bone.parent:
		return b_bone.parent.matrix_local.inverted() @ b_bone.matrix_local
	return b_bone.matrix_local


# Cache to store the last known action name/reference per object
_action_cache = {}


def set_fps_from_action_callback(scene, depsgraph):
	obj = bpy.context.object
	if obj and obj.animation_data:
		current_action = obj.animation_data.action
		last_action = _action_cache.get(obj.name)

		if current_action != last_action:
			_action_cache[obj.name] = current_action
			scene.frame_start = int(round(current_action.frame_range[0]))
			scene.frame_end = int(round(current_action.frame_range[1]))
			scene.render.fps = current_action.get("fps", 24)
			logging.info(f"Action changed to {current_action.name if current_action else 'None'} with {scene.render.fps} FPS")