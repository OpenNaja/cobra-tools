from generated.formats.buildingset.structs.BuildingSetRoot import BuildingSetRoot
from modules.formats.BaseFormat import MemStructLoader


class BuildingSetLoader(MemStructLoader):
    target_class = BuildingSetRoot
    extension = ".buildingset"
