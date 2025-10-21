from generated.formats.ridesettings.structs.RideSettingsRoot import RideSettingsRoot
from modules.formats.BaseFormat import MemStructLoader


class Ridesettings(MemStructLoader):
    target_class = RideSettingsRoot
    extension = ".ridesettings"
