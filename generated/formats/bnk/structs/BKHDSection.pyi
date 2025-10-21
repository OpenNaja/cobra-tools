from generated.array import Array
from generated.base_struct import BaseStruct


class BKHDSection(BaseStruct):
    length: int
    version: int
    id_a: int
    id_b: int
    constant_a: int
    constant_b: int
    unk: int
    zeroes: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
