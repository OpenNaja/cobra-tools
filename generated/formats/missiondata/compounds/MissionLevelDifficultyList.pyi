from generated.formats.missiondata.compounds.MissionLevelDifficulty import MissionLevelDifficulty
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MissionLevelDifficultyList(MemStruct):
    mission_level_difficulty_list: Pointer[MissionLevelDifficulty]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
