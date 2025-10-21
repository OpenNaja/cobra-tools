from generated.formats.cinematic.compounds.EventAttributes import EventAttributes
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Event(MemStruct):
    start_time: float
    b: float
    module_name: Pointer[str]
    attributes: Pointer[EventAttributes]
    duration: float
    d: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
