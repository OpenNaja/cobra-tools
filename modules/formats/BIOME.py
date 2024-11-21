from generated.formats.biome.structs.BiomeRoot import BiomeRoot
from generated.formats.biome.structs.BiomeArtSettingsRoot import BiomeArtSettingsRoot
from generated.formats.biome.structs.BiomeDesignSettingsRoot import BiomeDesignSettingsRoot
from generated.formats.biome.structs.BiomeAudioSettingsRoot import BiomeAudioSettingsRoot
from modules.formats.BaseFormat import MemStructLoader

class Biome(MemStructLoader):
	target_class = BiomeRoot
	extension = ".biome"

class BiomeArtSettings(MemStructLoader):
	target_class = BiomeArtSettingsRoot
	extension = ".biomeartsettings"

class BiomeAudioSettings(MemStructLoader):
	target_class = BiomeAudioSettingsRoot
	extension = ".biomeaudiosettings"

class BiomeDesignSettings(MemStructLoader):
	target_class = BiomeDesignSettingsRoot
	extension = ".biomedesignsettings"
