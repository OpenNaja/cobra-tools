from generated.array import Array
from generated.base_struct import BaseStruct


class ZTPreBones(BaseStruct):
    zeros: Array[int]
    unks: Array[int]
    unks_2: Array[int]
    floats: Array[float]
    unks_3: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
