from generated.formats.missiondata.compounds.MissionDataRoot import MissionDataRoot
from modules.formats.BaseFormat import MemStructLoader


class MissionDataLoader(MemStructLoader):
    target_class = MissionDataRoot
    extension = ".missiondata"
