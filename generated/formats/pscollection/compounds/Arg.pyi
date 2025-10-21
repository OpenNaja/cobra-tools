from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Arg(MemStruct):
    u_0: int
    arg_type: int
    arg_index: int
    u_1: int
    u_2: int
    arg_name: Pointer[str]
    u_4: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
