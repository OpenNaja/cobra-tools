from generated.formats.base.compounds.Vector3 import Vector3
from generated.formats.base.compounds.Vector4 import Vector4
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PathJoinPartResource(MemStruct):
    unk_points_1: ArrayPointer[Vector3]
    unk_points_2: ArrayPointer[Vector3]
    unk_vector: ArrayPointer[Vector4]
    unk_shorts: ArrayPointer[int]
    unk_points_3: ArrayPointer[Vector3]
    padding_1: int
    pathresource: Pointer[str]
    unk_byte_1: int
    unk_byte_2: int
    unk_byte_3: int
    num_points_1: int
    num_points_1_copy: int
    num_points_2: int
    num_points_2_copy: int
    num_points_3: int
    padding_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
