from generated.formats.particle.compounds.ParticleAtlasHeader import ParticleAtlasHeader
from modules.formats.BaseFormat import MemStructLoader


class ParticleAtlasLoader(MemStructLoader):
	target_class = ParticleAtlasHeader
	extension = ".particleatlas"
