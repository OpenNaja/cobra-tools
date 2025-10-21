from generated.array import Array
from generated.base_struct import BaseStruct


class WarExtraPart(BaseStruct):
    stuff: Array[int]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
