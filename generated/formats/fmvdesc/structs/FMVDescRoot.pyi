from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class FMVDescRoot(MemStruct):
    asset_path: Pointer[str]
    _zero_01: int
    _zero_02: int
    unk_65: int
    speed: float
    _zero_03: int
    _zero_04: int
    _zero_05: int
    _zero_06: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
