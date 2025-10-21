from generated.formats.ovl_base.structs.MemStruct import MemStruct


class JanitorBetweenArrays(MemStruct):
    a: float
    b: float
    c: int
    d: float
    e: float
    f: float
    g: float
    h: float
    i: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
