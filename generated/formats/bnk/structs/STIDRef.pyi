from generated.array import Array
from generated.base_struct import BaseStruct


class STIDRef(BaseStruct):
    bank_i_d: int
    stringsize: int
    name: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
