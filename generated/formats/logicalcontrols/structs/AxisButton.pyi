from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class AxisButton(MemStruct):
    button_name: Pointer[str]
    axis_name_x: Pointer[str]
    axis_name_y: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
