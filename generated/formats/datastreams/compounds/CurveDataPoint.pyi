from generated.formats.datastreams.enums.SubCurveType import SubCurveType
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class CurveDataPoint(MemStruct):
    x: float
    y: int
    sub_curve_type: SubCurveType
    subsequent_curve_param: int
    subsequent_curve_param_b: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
