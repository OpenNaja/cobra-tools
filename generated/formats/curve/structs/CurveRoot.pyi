from generated.formats.curve.structs.Key import Key
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class CurveRoot(MemStruct):
    keys: ArrayPointer[Key]
    count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
