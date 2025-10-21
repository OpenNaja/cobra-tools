from generated.formats.ovl_base.structs.MemStruct import MemStruct


class HbDoorCutout(MemStruct):
    height: float
    right: float
    left: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
