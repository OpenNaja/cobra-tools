from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.ovl_base.structs.ZStringList import ZStringList


class EnumnamerRoot(MemStruct):
    strings_count: int
    strings: Pointer[ZStringList]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
