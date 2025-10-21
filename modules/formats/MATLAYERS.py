from generated.formats.dinosaurmaterialvariants.structs.DinoEffectsHeader import DinoEffectsHeader
from generated.formats.dinosaurmaterialvariants.structs.DinoLayersHeader import DinoLayersHeader
from generated.formats.dinosaurmaterialvariants.structs.DinoPatternsHeader import DinoPatternsHeader
from generated.formats.dinosaurmaterialvariants.structs.DinoVariantsHeader import DinoVariantsHeader
from modules.formats.BaseFormat import MemStructLoader


class MatlayersLoader(MemStructLoader):
	target_class = DinoLayersHeader
	extension = ".dinosaurmateriallayers"


class MatvarsLoader(MemStructLoader):
	target_class = DinoVariantsHeader
	extension = ".dinosaurmaterialvariants"


class MateffsLoader(MemStructLoader):
	target_class = DinoEffectsHeader
	extension = ".dinosaurmaterialeffects"


class MatpatsLoader(MemStructLoader):
	target_class = DinoPatternsHeader
	extension = ".dinosaurmaterialpatterns"
