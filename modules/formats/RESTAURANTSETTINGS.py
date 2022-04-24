from generated.formats.restaurantsettings.compound.RestaurantSettingsRoot import RestaurantSettingsRoot
from modules.formats.BaseFormat import MemStructLoader


class Restaurantsettings(MemStructLoader):
    target_class = RestaurantSettingsRoot
    extension = ".restaurantsettings"
