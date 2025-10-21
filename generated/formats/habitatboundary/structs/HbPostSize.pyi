from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class HbPostSize(MemStruct):
    front_back: float
    left_right: float
    top: float

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
