from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.structs.Vector3 import Vector3


class Str48(BaseStruct):
    quat: Array[float]
    v_1: Vector3
    v_2: Vector3
    a: int
    b: int
    index: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
