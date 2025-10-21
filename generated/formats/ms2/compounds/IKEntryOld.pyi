from generated.array import Array
from generated.base_struct import BaseStruct


class IKEntryOld(BaseStruct):
    name: int
    index: int
    parent: int
    child: int
    length: int
    parent_again: int
    floats: Array[float]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
