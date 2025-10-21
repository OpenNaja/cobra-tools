from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class HbUiOptions(MemStruct):
    straight_curve: bool
    windows: bool

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
