from generated.formats.ovl_base.structs.MemStruct import MemStruct


class HbPostPos(MemStruct):
    right: float
    left: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
