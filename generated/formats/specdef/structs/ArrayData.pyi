from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.specdef.enums.SpecdefDtype import SpecdefDtype
from generated.formats.specdef.structs.Data import Data


class ArrayData(MemStruct):
    item: Pointer[Data]
    dtype: SpecdefDtype
    unused: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
