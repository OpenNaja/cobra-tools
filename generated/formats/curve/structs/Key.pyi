from generated.formats.ovl_base.structs.MemStruct import MemStruct


class Key(MemStruct):
    time: float
    value: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
