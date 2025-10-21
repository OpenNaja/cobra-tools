from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class FxDataSettings(MemStruct):
    unk_0: int
    unk_ptr_0: Pointer[str]
    unk_ptr_1: Pointer[str]
    unk_1: int
    unk_2: int
    unk_3: int
    unk_4: int
    unk_5: int
    unk_6: int
    unk_7: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
