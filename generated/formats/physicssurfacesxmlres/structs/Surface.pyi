from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class Surface(MemStruct):
    surface_name: Pointer[str]
    float_1: float
    float_2: float
    float_3: float
    float_4: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
