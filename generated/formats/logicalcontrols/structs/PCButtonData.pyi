from generated.formats.logicalcontrols.structs.ButtonStr import ButtonStr
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class PCButtonData(MemStruct):
    keys: ArrayPointer[ButtonStr]
    key_count: int
    key_flags: int
    unkown: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
