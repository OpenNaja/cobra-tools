from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class MotiongraphVar(MemStruct):
    var_name: Pointer[str]
    a: int
    b_0: float
    b_1: float
    c: int
    d: int
    e: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
