from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ByteVector3(MemStruct):
    x: int
    y: int
    z: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
