from generated.formats.ovl_base.structs.MemStruct import MemStruct


class DetailStruct(MemStruct):
    index: int
    x: float
    y: float
    z: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
