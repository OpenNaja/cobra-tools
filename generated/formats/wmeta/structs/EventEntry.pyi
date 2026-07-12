from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class EventEntry(MemStruct):
    stop_start_fnv: int
    padding: int
    event_name: Pointer[str]
    float: float
    flag_0: int
    flag_1: int
    flag_2: int
    start_name: Pointer[str]
    zero_2: int
    start_fnv: int
    event_fnv: int
    zero_4: int
    f_0: float
    f_1: float
    u_4: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
