from generated.formats.ovl_base.structs.MemStruct import MemStruct


class CurveKey(MemStruct):
    time: float
    x: float
    y: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
