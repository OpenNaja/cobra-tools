from generated.formats.ovl_base.structs.MemStruct import MemStruct


class Pc2TexMip(MemStruct):
    offset: int
    size: int
    num_weaves_x: int
    num_weaves_y: int
    do_weave: int
    ff: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
