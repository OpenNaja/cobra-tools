from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class MotiongraphVarNew(MemStruct):
    var_name: Pointer[str]
    a: int
    b: float
    c: float
    d: int
    e: float
    f: int
    g: int
    name_2: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
