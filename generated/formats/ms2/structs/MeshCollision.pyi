from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.ms2.structs.Matrix33 import Matrix33
from generated.formats.ms2.structs.MeshCollisionIndex import MeshCollisionIndex


class MeshCollision(BaseStruct):
    rotation: Matrix33
    offset: Vector3
    indices: Array[MeshCollisionIndex]
    unk_2: Array[int]
    vertex_count: int
    tri_count: int
    bounds_min: Vector3
    bounds_max: Vector3
    flag_0: int
    flag_1: int
    is_optimized: int
    zeros_1: Array[int]
    tris_switch: int
    ff: int
    zeros_2: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
