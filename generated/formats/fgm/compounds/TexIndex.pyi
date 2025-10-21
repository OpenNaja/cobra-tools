from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class TexIndex(MemStruct):
    _tex_index: int
    array_index: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
