from generated.formats.researchdata.structs.ResearchRoot import ResearchRoot
from modules.formats.BaseFormat import MemStructLoader

class ResearchDataLoader(MemStructLoader):
	target_class = ResearchRoot
	extension = ".researchdata"