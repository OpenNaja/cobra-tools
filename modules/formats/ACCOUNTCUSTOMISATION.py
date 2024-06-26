from generated.formats.accountcustomisation.compounds.AccountCustomisationRoot import AccountCustomisationRoot
from modules.formats.BaseFormat import MemStructLoader


class AccountCustomisationLoader(MemStructLoader):
    target_class = AccountCustomisationRoot
    extension = ".accountcustomisation"
