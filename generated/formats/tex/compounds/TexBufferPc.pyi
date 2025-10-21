from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class TexBufferPc(MemStruct):
    width: int
    height: int
    num_tiles: int
    num_mips: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
