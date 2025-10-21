from generated.formats.ovl_base.structs.MemStruct import MemStruct


class BrushRoot(MemStruct):
    _zero: int
    num_pixels: int
    x: int
    y: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
