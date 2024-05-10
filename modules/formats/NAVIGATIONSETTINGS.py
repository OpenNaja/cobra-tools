from generated.formats.navigationsettings.compounds.NavigationSettingsRoot import NavigationSettingsRoot
from modules.formats.BaseFormat import MemStructLoader


class NavigationSettingsLoader(MemStructLoader):
    target_class = NavigationSettingsRoot
    extension = ".navigationsettings"
