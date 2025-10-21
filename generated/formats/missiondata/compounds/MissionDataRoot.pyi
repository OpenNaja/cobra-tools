from generated.formats.missiondata.compounds.MissionLevel import MissionLevel
from generated.formats.missiondata.compounds.MissionLevelDifficultyList import MissionLevelDifficultyList
from generated.formats.missiondata.compounds.MissionLevelUnknownList import MissionLevelUnknownList
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.ovl_base.compounds.ZStringList import ZStringList


class MissionDataRoot(MemStruct):
    mission_ui_name: Pointer[str]
    mission_ui_description: Pointer[str]
    mission_ui_description_pause: Pointer[str]
    mission_id: Pointer[str]
    mission_name: Pointer[str]
    mission_objective_fail_generic: Pointer[str]
    mission_objective_success_generic: Pointer[str]
    mission_level_list: ArrayPointer[MissionLevel]
    mission_level_count: int
    mission_level_ai_strategy: Pointer[str]
    mission_level_unknown_01: int
    mission_level_unknown_02: int
    mission_level_unknown_03: int
    mission_level_unknown_04: int
    mission_level_unknown_05: int
    mission_level_unknown_list: ArrayPointer[MissionLevelUnknownList]
    mission_level_unknown_count: int
    mission_level_unknown_06: int
    mission_level_unknown_07: int
    mission_level_difficulty_list: ArrayPointer[MissionLevelDifficultyList]
    mission_level_difficulty_count: int
    mission_level_camera: Pointer[ZStringList]
    mission_level_camera_count: int
    mission_campaign_name: Pointer[str]
    mission_mission_name: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
