from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.ovl_base.structs.ZStringList import ZStringList


class SemanticFlexiColoursRoot(MemStruct):
    names: Pointer[ZStringList]
    names_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
