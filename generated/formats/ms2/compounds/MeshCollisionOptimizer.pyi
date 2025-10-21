from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.compounds.Vector3 import Vector3
from generated.formats.ms2.compounds.MeshCollisionChunk import MeshCollisionChunk


class MeshCollisionOptimizer(BaseStruct):
    bounds_min_repeat: Vector3
    bounds_max_repeat: Vector3
    tri_flags_count: int
    chunks_count: int
    some_index: int
    zeros: Array[int]
    chunks: Array[MeshCollisionChunk]
    tris_salt: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
