from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class EventEntry(MemStruct):
    hash: int
    zero: int
    block_name: Pointer[str]
    zero_2: int
    size: int
    flag_0: int
    flag_1: int
    flag_2: int
    zero_3: int
    flag_3: int
    hash_b: int
    hash_c: int
    zero_4: int
    u_2: int
    u_1: int
    u_4: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
