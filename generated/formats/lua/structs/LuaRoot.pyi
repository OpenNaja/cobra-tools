from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class LuaRoot(MemStruct):
    lua_size: int
    sixteenk: int
    hash: int
    zero_0: int
    source_path: Pointer[str]
    likely_alignment: Pointer[str]
    zero_1: int
    zero_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
