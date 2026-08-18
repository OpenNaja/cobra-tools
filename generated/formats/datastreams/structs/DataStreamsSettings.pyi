from generated.formats.datastreams.structs.CurveDataPoint import CurveDataPoint
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class DataStreamsSettings(MemStruct):
    c_0: int
    c_1: int
    z_0: int
    name_a: Pointer[str]
    name_b: Pointer[str]
    z_1: int
    z_2: int
    data_count: int
    data: ArrayPointer[CurveDataPoint]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
