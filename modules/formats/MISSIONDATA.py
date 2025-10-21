from generated.formats.missiondata.structs.MissionDataRoot import MissionDataRoot
from modules.formats.BaseFormat import MemStructLoader


class MissionDataLoader(MemStructLoader):
    target_class = MissionDataRoot
    extension = ".missiondata"
