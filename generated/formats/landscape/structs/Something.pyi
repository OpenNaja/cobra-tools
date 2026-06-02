from generated.array import Array
from generated.base_struct import BaseStruct


class Something(BaseStruct):
    flo_22: Array[float]
    junk_22: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
