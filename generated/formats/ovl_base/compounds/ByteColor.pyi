from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ByteColor(MemStruct):
    r: int
    g: int
    b: int
    a: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
