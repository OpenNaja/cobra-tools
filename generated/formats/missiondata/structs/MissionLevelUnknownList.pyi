from generated.formats.missiondata.structs.MissionLevelUnknown import MissionLevelUnknown
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class MissionLevelUnknownList(MemStruct):
    mission_level_unknown_list: Pointer[MissionLevelUnknown]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
