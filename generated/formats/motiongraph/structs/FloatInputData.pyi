from generated.formats.motiongraph.structs.OptionalVarAndCurve import OptionalVarAndCurve
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class FloatInputData(MemStruct):
    float: float
    optional_var_and_curve_count: int
    optional_var_and_curve: ArrayPointer[OptionalVarAndCurve]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
