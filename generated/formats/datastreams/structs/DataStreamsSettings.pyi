from generated.formats.datastreams.structs.CurveDataPoint import CurveDataPoint
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class DataStreamsSettings(MemStruct):
    name_a: Pointer[str]
    name_b: Pointer[str]
    z_0: int
    z_1: int
    count: int
    data: ArrayPointer[CurveDataPoint]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
