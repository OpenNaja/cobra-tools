from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.specdef.compounds.Data import Data
from generated.formats.specdef.enums.SpecdefDtype import SpecdefDtype


class ArrayData(MemStruct):
    item: Pointer[Data]
    dtype: SpecdefDtype
    unused: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
