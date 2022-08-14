from generated.formats.restaurantsettings.compounds.RestaurantSettingsRoot import RestaurantSettingsRoot
from modules.formats.BaseFormat import MemStructLoader


class Restaurantsettings(MemStructLoader):
    target_class = RestaurantSettingsRoot
    extension = ".restaurantsettings"
