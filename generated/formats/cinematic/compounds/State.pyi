from generated.formats.cinematic.compounds.EventsList import EventsList
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


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
