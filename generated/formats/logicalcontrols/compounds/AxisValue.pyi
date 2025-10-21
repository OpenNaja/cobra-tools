from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class AxisValue(MemStruct):
    axis_name: Pointer[str]
    button_1_name: Pointer[str]
    button_2_name: Pointer[str]
    unk: int
    combined_value_name: Pointer[str]
    single_value_1_name: Pointer[str]
    single_value_2_name: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
