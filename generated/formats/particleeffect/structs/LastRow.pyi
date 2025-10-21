from generated.formats.ovl_base.structs.MemStruct import MemStruct


class LastRow(MemStruct):
    unk_07: int
    unk_08: int
    unk_09: int
    unk_10: int
    unk_11: int
    unk_12: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
