from generated.formats.terrainindexeddetaillayers.compounds.TerrainIndexedDetailLayersRoot import TerrainIndexedDetailLayersRoot
from modules.formats.BaseFormat import MemStructLoader

class TerrainIndexedDetailLayersLoader(MemStructLoader):
	target_class = TerrainIndexedDetailLayersRoot
	extension = ".terrainindexeddetaillayers"