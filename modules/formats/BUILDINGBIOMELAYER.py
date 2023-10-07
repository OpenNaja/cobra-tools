from generated.formats.buildingbiomelayer.compounds.BuildingBiomeLayerRoot import BuildingBiomeLayerRoot
from modules.formats.BaseFormat import MemStructLoader


class BuildingBiomeLayerLoader(MemStructLoader):
    target_class = BuildingBiomeLayerRoot
    extension = ".buildingbiomelayer"
