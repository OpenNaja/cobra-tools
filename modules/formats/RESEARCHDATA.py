from generated.formats.researchdata.compounds.ResearchRoot import ResearchRoot
from modules.formats.BaseFormat import MemStructLoader

class ResearchDataLoader(MemStructLoader):
	target_class = ResearchRoot
	extension = ".researchdata"