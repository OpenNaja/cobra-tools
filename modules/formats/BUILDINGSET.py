from generated.formats.buildingset.compounds.BuildingSetRoot import BuildingSetRoot
from modules.formats.BaseFormat import MemStructLoader


class BuildingSetLoader(MemStructLoader):
    target_class = BuildingSetRoot
    extension = ".buildingset"
