from generated.formats.ovl_base.structs.MemStruct import MemStruct


class FloatColor(MemStruct):
    r: float
    g: float
    b: float
    a: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
