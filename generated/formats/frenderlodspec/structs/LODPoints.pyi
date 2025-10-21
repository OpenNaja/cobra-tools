from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class LODPoints(MemStruct):
    discard_at_lod: int
    max_lods: int
    lod_points: Array[float]
    pixel_size_off: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
