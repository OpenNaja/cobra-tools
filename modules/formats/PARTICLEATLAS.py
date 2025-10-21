from generated.formats.particleatlas.structs.ParticleAtlasRoot import ParticleAtlasRoot
from modules.formats.BaseFormat import MemStructLoader

class ParticleAtlasLoader(MemStructLoader):
	target_class = ParticleAtlasRoot
	extension = ".particleatlas"

