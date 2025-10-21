from generated.formats.ovl_base.structs.MemStruct import MemStruct


class UIntPair(MemStruct):
    value_0: int
    value_1: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
