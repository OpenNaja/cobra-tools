from generated.formats.motiongraph.compounds.CurveDataPoint import CurveDataPoint
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class CurveData(MemStruct):
    count: int
    points: ArrayPointer[CurveDataPoint]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
