from generated.formats.ovl_base.structs.MemStruct import MemStruct


class TexBuffer(MemStruct):
    offset: int
    size: int
    first_mip: int
    mip_count: int
    padding_0: int
    padding_1: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
