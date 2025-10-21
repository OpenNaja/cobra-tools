from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.trackstation.compounds.End import End
from generated.formats.trackstation.compounds.Start import Start


class FlumeInfo(MemStruct):
    starts: ArrayPointer[Start]
    starts_count: int
    ends: ArrayPointer[End]
    ends_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
