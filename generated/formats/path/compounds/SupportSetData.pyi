from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class SupportSetData(MemStruct):
    unk_index: int
    unk_int_1: int
    unk_int_2: int
    unk_float_1: float
    unk_int_3: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
