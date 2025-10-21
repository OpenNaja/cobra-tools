from generated.array import Array
from generated.base_struct import BaseStruct


class UncompressedManiDataPC2(BaseStruct):
    z_0: Array[int]
    c_0: int
    z_1: Array[int]
    c_2: int
    z_2: Array[int]
    target_bone_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
