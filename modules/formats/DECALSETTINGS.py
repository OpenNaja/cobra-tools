from generated.formats.decalsettings.compounds.DecalSettingsRoot import DecalSettingsRoot
from modules.formats.BaseFormat import MemStructLoader


class DecalSettingsettingsLoader(MemStructLoader):
	target_class = DecalSettingsRoot
	extension = ".decalsettings"
