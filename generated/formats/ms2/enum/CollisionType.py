from source.formats.base.basic import fmt_member
from generated.formats.base.enum import UintEnum


class CollisionType(UintEnum):
	SPHERE = 0
	BOUNDING_BOX = 1
	CAPSULE = 2
	CYLINDER = 3
	CONVEX_HULL = 7
	CONVEX_HULL_P_C = 8
	# widgetball_test.mdl2, Ball_Hitcheck not supported, seems to be another collision mesh used in JWE redwoods
	MESH_COLLISION = 10
	# ?
	UNK_RHINO = 11
