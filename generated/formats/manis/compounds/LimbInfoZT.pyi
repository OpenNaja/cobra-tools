from generated.array import Array
from generated.base_struct import BaseStruct


class LimbInfoZT(BaseStruct):
    footplant: int
    index_b: int
    zero_0: int
    count_a: int
    count_b: int
    zero_1: int
    zeros: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
