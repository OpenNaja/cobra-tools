from generated.formats.terraindetaillayers.structs.TerrainDetailLayersRoot import TerrainDetailLayersRoot
from modules.formats.BaseFormat import MemStructLoader

class TerrainDetailLayersLoader(MemStructLoader):
	target_class = TerrainDetailLayersRoot
	extension = ".terraindetaillayers"