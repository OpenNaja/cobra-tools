from generated.formats.missiondata.compounds.MissionLevelUnknown import MissionLevelUnknown
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MissionLevelUnknownList(MemStruct):
    mission_level_unknown_list: Pointer[MissionLevelUnknown]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
