from generated.formats.motiongraph.structs.CurveDataPoint import CurveDataPoint
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class CurveData(MemStruct):
    count: int
    points: ArrayPointer[CurveDataPoint]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
