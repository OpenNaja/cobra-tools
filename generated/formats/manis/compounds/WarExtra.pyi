from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.compounds.WarExtraPart import WarExtraPart


class WarExtra(BaseStruct):
    zeros: Array[int]
    stuff: Array[WarExtraPart]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
