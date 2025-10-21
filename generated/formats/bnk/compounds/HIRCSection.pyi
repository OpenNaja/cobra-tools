from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.compounds.HircPointer import HircPointer


class HIRCSection(BaseStruct):
    length: int
    count: int
    hirc_pointers: Array[HircPointer]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
