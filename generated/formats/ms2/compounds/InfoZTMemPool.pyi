from generated.array import Array
from generated.base_struct import BaseStruct


class InfoZTMemPool(BaseStruct):
    unk_count: int
    unks: Array[Array[int]]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
