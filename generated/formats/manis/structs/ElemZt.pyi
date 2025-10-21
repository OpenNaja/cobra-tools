from generated.array import Array
from generated.base_struct import BaseStruct


class ElemZt(BaseStruct):
    floats: Array[float]
    a: int
    b: int
    c: int
    d: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
