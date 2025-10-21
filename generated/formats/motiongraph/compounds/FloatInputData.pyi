from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FloatInputData(MemStruct):
    float: float
    optional_var_and_curve_count: int
    optional_var_and_curve: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
