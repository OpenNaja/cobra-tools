from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class FxDataName(MemStruct):
    unk_0: int
    unk_ptr: Pointer[str]
    unk_1: int
    unk_2: int
    unk_3: int
    unk_4: int
    unk_5: int
    unk_6: int
    unk_7: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
