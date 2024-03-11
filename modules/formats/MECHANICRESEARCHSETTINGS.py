from generated.formats.mechanicresearch.compounds.ResearchRoot import ResearchRoot
from modules.formats.BaseFormat import MemStructLoader


class MechanicresearchsettingsLoader(MemStructLoader):
	target_class = ResearchRoot
	extension = ".mechanicresearchsettings"
