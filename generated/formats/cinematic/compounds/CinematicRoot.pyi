from generated.formats.cinematic.compounds.CinematicData import CinematicData
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.ovl_base.compounds.ZStringList import ZStringList


class CinematicRoot(MemStruct):
    names: Pointer[ZStringList]
    names_count: int
    data: ArrayPointer[CinematicData]
    data_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
