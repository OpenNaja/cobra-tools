from generated.formats.mechanicresearch.structs.ResearchRoot import ResearchRoot
from modules.formats.BaseFormat import MemStructLoader


class MechanicresearchsettingsLoader(MemStructLoader):
	target_class = ResearchRoot
	extension = ".mechanicresearchsettings"
