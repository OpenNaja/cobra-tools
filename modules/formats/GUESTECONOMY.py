from generated.formats.guesteconomy.compound.GuestEconomyRoot import GuestEconomyRoot
from modules.formats.BaseFormat import MemStructLoader


class GuestEconomyLoader(MemStructLoader):
    extension = ".guesteconomy"
    target_class = GuestEconomyRoot
