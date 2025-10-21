from generated.formats.accountlevelsdata.compounds.AccountLevel import AccountLevel
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class AccountLevelsDataRoot(MemStruct):
    account_level_version: int
    account_levels: ArrayPointer[AccountLevel]
    account_levels_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
