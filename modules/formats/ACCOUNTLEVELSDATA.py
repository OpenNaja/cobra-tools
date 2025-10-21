from generated.formats.accountlevelsdata.structs.AccountLevelsDataRoot import AccountLevelsDataRoot
from modules.formats.BaseFormat import MemStructLoader


class AccountLevelsDataLoader(MemStructLoader):
    target_class = AccountLevelsDataRoot
    extension = ".accountlevelsdata"
