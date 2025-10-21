from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class IslandRoot(MemStruct):
    path_name: Pointer[str]
    a: float
    b: float
    count: int
    zero: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
