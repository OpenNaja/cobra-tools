from generated.formats.ovl_base.structs.MemStruct import MemStruct


class FloatData(MemStruct):
    imin: float
    imax: float
    ivalue: float
    ioptional: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
