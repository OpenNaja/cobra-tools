from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Mipmap(MemStruct):
    offset: int
    size: int
    size_array: int
    size_scan: int
    size_data: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
