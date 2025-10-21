from generated.formats.vendingmachineinteractionsettings.structs.VendingMachineInteractionSettingsRoot import VendingMachineInteractionSettingsRoot
from modules.formats.BaseFormat import MemStructLoader


class VendingMachineInteractionSettings(MemStructLoader):
    target_class = VendingMachineInteractionSettingsRoot
    extension = ".vendingmachineinteractionsettings"
