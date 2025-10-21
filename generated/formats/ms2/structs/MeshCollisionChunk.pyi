from generated.array import Array
from generated.base_struct import BaseStruct


class MeshCollisionChunk(BaseStruct):
    a: Array[int]
    tri_indices: Array[int]
    min_of_indices: int
    num_used_tri_slots: int
    salt_index: int
    consts: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
