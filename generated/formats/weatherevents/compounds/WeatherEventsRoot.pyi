from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.weatherevents.compounds.WeatherEventData import WeatherEventData


class WeatherEventsRoot(MemStruct):
    resource_name: Pointer[str]
    default_event_name: Pointer[str]
    transition_time: float
    unknown_1: float
    event_list: ArrayPointer[WeatherEventData]
    event_count: int
    unknown_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
