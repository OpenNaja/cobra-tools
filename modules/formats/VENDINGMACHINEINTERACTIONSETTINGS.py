from generated.formats.vendingmachineinteractionsettings.compounds.VendingMachineInteractionSettingsRoot import VendingMachineInteractionSettingsRoot
from modules.formats.BaseFormat import MemStructLoader


class VendingMachineInteractionSettings(MemStructLoader):
    target_class = VendingMachineInteractionSettingsRoot
    extension = ".vendingmachineinteractionsettings"
