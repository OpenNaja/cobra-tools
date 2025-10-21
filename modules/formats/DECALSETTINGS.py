from generated.formats.decalsettings.structs.DecalSettingsRoot import DecalSettingsRoot
from modules.formats.BaseFormat import MemStructLoader


class DecalSettingsettingsLoader(MemStructLoader):
	target_class = DecalSettingsRoot
	extension = ".decalsettings"
