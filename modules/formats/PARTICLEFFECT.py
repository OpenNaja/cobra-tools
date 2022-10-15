from generated.formats.particleeffect.compounds.ParticleEffectRoot import ParticleEffectRoot
from modules.formats.BaseFormat import MemStructLoader

class ParticleEffetLoader(MemStructLoader):
	target_class = ParticleEffectRoot
	extension = ".particleeffect"
