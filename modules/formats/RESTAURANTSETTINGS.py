from generated.formats.restaurantsettings.structs.RestaurantSettingsRoot import RestaurantSettingsRoot
from modules.formats.BaseFormat import MemStructLoader


class Restaurantsettings(MemStructLoader):
    target_class = RestaurantSettingsRoot
    extension = ".restaurantsettings"
