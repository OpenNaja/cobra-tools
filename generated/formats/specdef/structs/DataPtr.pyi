from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.specdef.structs.Data import Data


class DataPtr(MemStruct):
    data_ptr: Pointer[Data]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
