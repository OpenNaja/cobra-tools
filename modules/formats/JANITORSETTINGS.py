from generated.formats.janitorsettings.compound.JanitorSettingsRoot import JanitorSettingsRoot
from modules.formats.BaseFormat import MemStructLoader


class Janitorsettings(MemStructLoader):
	target_class = JanitorSettingsRoot
	extension = ".janitorsettings"
