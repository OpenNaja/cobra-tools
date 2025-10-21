from generated.base_struct import BaseStruct


class LodInfo(BaseStruct):
    full: int
    half: int
    lod_index: int
    distance: float
    stream_index: int
    bone_index: int
    first_object_index: int
    first_object_index_1: int
    first_object_index_2: int
    last_object_index: int
    vertex_count: int
    tri_index_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
