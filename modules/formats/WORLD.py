from generated.formats.world.compound.WorldHeader import WorldHeader
from modules.formats.BaseFormat import MemStructLoader


class WorldLoader(MemStructLoader):
    target_class = WorldHeader
