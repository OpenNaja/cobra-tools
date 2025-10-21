from generated.array import Array
from generated.formats.base.structs.Vector3 import Vector3
from generated.formats.base.structs.Vector4 import Vector4
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class WsmHeader(MemStruct):
    duration: float
    frame_count: int
    unknowns: Array[float]
    locs: ArrayPointer[Vector3]
    quats: ArrayPointer[Vector4]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
