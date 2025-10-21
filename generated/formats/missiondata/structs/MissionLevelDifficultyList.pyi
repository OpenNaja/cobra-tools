from generated.formats.missiondata.structs.MissionLevelDifficulty import MissionLevelDifficulty
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class MissionLevelDifficultyList(MemStruct):
    mission_level_difficulty_list: Pointer[MissionLevelDifficulty]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
