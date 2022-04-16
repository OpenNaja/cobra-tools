from generated.formats.dinosaurmaterialvariants.compound.DinoEffectsHeader import DinoEffectsHeader
from generated.formats.dinosaurmaterialvariants.compound.DinoLayersHeader import DinoLayersHeader
from generated.formats.dinosaurmaterialvariants.compound.DinoPatternsHeader import DinoPatternsHeader
from generated.formats.dinosaurmaterialvariants.compound.DinoVariantsHeader import DinoVariantsHeader
from modules.formats.BaseFormat import MemStructLoader


class MatlayersLoader(MemStructLoader):
	target_class = DinoLayersHeader


class MatvarsLoader(MemStructLoader):
	target_class = DinoVariantsHeader


class MateffsLoader(MemStructLoader):
	target_class = DinoEffectsHeader


class MatpatsLoader(MemStructLoader):
	target_class = DinoPatternsHeader
