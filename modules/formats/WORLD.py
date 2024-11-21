from generated.formats.world.compounds.WorldHeader import WorldHeader
from generated.formats.world.compounds.WorldArtSettingsHeader import WorldArtSettingsHeader
from generated.formats.world.compounds.WorldSharedSettingsHeader import WorldSharedSettingsHeader 
from modules.formats.BaseFormat import MemStructLoader


class WorldLoader(MemStructLoader):
    target_class = WorldHeader
    extension = ".world"


# Introduced for PC2 
class WorldSharedSettingsLoader(MemStructLoader):
    target_class = WorldSharedSettingsHeader
    extension = ".worldsharedsettings"

# Introduced for PC2 
class WorldArtSettingsLoader(MemStructLoader):
    target_class = WorldArtSettingsHeader
    extension = ".worldartsettings"
