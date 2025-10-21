from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class EventAttributes(MemStruct):
    anim_name: Pointer[str]
    event_name: Pointer[str]
    empty_string: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
