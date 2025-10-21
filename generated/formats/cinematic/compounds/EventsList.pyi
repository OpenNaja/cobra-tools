from generated.formats.cinematic.compounds.Event import Event
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class EventsList(MemStruct):
    events: ArrayPointer[Event]
    num_events: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
