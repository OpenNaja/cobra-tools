from generated.formats.ridesettings.compounds.RideSettingsRoot import RideSettingsRoot
from modules.formats.BaseFormat import MemStructLoader


class Ridesettings(MemStructLoader):
    target_class = RideSettingsRoot
    extension = ".ridesettings"
