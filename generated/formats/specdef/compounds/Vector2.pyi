from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Vector2(MemStruct):
    x: float
    y: float
    ioptional: int
    unused: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
