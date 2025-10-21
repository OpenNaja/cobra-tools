from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Lod(MemStruct):
    a: int
    b: int
    c: int
    distance: float
    e: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
