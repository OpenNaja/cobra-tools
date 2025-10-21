from generated.formats.motiongraph.structs.CurveData import CurveData
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class DataStreamResourceData(MemStruct):
    curve_type: int
    ds_name: Pointer[str]
    type: Pointer[str]
    bone_i_d: Pointer[str]
    location: Pointer[str]
    curve: CurveData

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
