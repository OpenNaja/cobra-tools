from generated.formats.animalresearch.compounds.ResearchRoot import ResearchRoot
from generated.formats.animalresearch.compounds.ResearchStartRoot import ResearchStartRoot
from modules.formats.BaseFormat import MemStructLoader


class AnimalresearchunlockssettingsLoader(MemStructLoader):
	target_class = ResearchRoot
	extension = ".animalresearchunlockssettings"


class AnimalresearchstartunlockedssettingsLoader(MemStructLoader):
	target_class = ResearchStartRoot
	extension = ".animalresearchstartunlockedsettings"
