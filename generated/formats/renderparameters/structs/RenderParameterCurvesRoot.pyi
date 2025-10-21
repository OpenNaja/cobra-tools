from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.renderparameters.structs.CurveParamList import CurveParamList


class RenderParameterCurvesRoot(MemStruct):
    param_name: Pointer[str]
    params: Pointer[CurveParamList]
    params_count: int
    unk: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
