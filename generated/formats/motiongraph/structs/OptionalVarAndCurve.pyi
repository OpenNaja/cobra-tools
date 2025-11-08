from generated.formats.motiongraph.structs.CurveData import CurveData
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class OptionalVarAndCurve(MemStruct):
    var_name: Pointer[str]
    curve: CurveData

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
