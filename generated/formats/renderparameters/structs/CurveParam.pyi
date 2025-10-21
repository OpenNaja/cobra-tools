from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.renderparameters.enums.RenderParameterType import RenderParameterType
from generated.formats.renderparameters.structs.CurveList import CurveList


class CurveParam(MemStruct):
    attribute_name: Pointer[str]
    dtype: RenderParameterType
    do_interpolation: int
    samples: Pointer[CurveList]
    samples_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
