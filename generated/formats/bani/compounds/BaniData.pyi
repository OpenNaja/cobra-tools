from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class BaniData(MemStruct):
    a: int
    b: int
    unk: float
    increment: int
    zero: int
    num_bones: int
    index_reversed: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
