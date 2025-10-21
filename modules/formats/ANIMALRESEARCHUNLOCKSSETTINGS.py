from generated.formats.animalresearch.structs.ResearchRoot import ResearchRoot
from generated.formats.animalresearch.structs.ResearchStartRoot import ResearchStartRoot
from modules.formats.BaseFormat import MemStructLoader


class AnimalresearchunlockssettingsLoader(MemStructLoader):
	target_class = ResearchRoot
	extension = ".animalresearchunlockssettings"


class AnimalresearchstartunlockedssettingsLoader(MemStructLoader):
	target_class = ResearchStartRoot
	extension = ".animalresearchstartunlockedsettings"
