from generated.base_enum import BaseEnum


class CollisionType(BaseEnum):
    SPHERE: CollisionType
    BOUNDING_BOX: CollisionType
    CAPSULE: CollisionType
    CYLINDER: CollisionType
    CONVEX_HULL: CollisionType
    CONVEX_HULL_P_C: CollisionType
    MESH_COLLISION: CollisionType
    UNK_RHINO: CollisionType
