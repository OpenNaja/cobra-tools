from generated.formats.particleatlas.compounds.ParticleAtlasRoot import ParticleAtlasRoot
from modules.formats.BaseFormat import MemStructLoader

class ParticleAtlasLoader(MemStructLoader):
	target_class = ParticleAtlasRoot
	extension = ".particleatlas"

