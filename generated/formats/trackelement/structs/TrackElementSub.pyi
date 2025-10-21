from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class TrackElementSub(MemStruct):
    catwalk_right_lsm: Pointer[str]
    catwalk_left_lsm: Pointer[str]
    catwalk_both_lsm: Pointer[str]
    unk_0: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
