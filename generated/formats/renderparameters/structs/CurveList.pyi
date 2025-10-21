from generated.array import Array
from generated.formats.ovl_base.structs.NestedPointers import NestedPointers
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.renderparameters.structs.KeyPoint import KeyPoint


class CurveList(NestedPointers):
    ptrs: Array[Pointer[KeyPoint]]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
