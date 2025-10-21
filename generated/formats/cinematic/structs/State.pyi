from generated.formats.cinematic.structs.EventsList import EventsList
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class State(MemStruct):
    abstract_name: Pointer[str]
    concrete_name: Pointer[str]
    prefab_name: Pointer[str]
    a: int
    b: int
    c: int
    events_list: Pointer[EventsList]
    d: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
