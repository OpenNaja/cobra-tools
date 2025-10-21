from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ridesettings.structs.Pair import Pair


class RideSettingsRoot(MemStruct):
    unk_0: float
    unk_1: int
    array_1: ArrayPointer[Pair]
    count: int
    pad_0: int
    pad_1: int
    pad_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
