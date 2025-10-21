from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MissionLevelDifficulty(MemStruct):
    mission_level_difficulty_1: Pointer[str]
    mission_level_difficulty_2: Pointer[str]
    mission_level_difficulty_3: Pointer[str]
    mission_level_difficulty_4: Pointer[str]
    mission_level_difficulty_5: Pointer[str]
    mission_level_difficulty_6: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
