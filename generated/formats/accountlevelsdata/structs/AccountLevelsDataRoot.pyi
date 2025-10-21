from generated.formats.accountlevelsdata.structs.AccountLevel import AccountLevel
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class AccountLevelsDataRoot(MemStruct):
    account_level_version: int
    account_levels: ArrayPointer[AccountLevel]
    account_levels_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
