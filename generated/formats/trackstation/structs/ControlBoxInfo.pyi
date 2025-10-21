from generated.array import Array
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class ControlBoxInfo(MemStruct):
    front_panel: Pointer[str]
    left_panel: Pointer[str]
    right_panel: Pointer[str]
    position: Array[float]
    unkown_float_1: float
    unkown_float_2: float
    unkown_float_3: float
    unkown_float_4: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
