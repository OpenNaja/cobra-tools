from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.Vector3 import Vector3


class WeirdElementOne(BaseStruct):
    float_0: float
    vec_0: Vector3
    zeros_0: Array[int]
    vec_1: Vector3
    countb: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
