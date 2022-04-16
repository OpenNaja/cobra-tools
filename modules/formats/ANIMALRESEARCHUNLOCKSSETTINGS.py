from generated.formats.animalresearch.compound.ResearchRoot import ResearchRoot
from generated.formats.animalresearch.compound.ResearchStartRoot import ResearchStartRoot
from modules.formats.BaseFormat import MemStructLoader


class AnimalresearchunlockssettingsLoader(MemStructLoader):
	target_class = ResearchRoot


class AnimalresearchstartunlockedssettingsLoader(MemStructLoader):
	target_class = ResearchStartRoot
