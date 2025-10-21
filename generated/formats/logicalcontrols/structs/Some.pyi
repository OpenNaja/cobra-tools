from generated.formats.logicalcontrols.structs.SomeData import SomeData
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class Some(MemStruct):
    some_name: Pointer[str]
    some_data: ArrayPointer[SomeData]
    some_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
