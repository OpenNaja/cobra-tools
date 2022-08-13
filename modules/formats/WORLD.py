from generated.formats.world.compounds.WorldHeader import WorldHeader
from modules.formats.BaseFormat import MemStructLoader


class WorldLoader(MemStructLoader):
    target_class = WorldHeader
    extension = ".world"
