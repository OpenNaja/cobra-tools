from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Pair(MemStruct):
    value_0: int
    value_1: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
