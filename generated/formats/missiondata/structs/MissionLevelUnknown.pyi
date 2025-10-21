from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class MissionLevelUnknown(MemStruct):
    mission_level_unknown_data_flags: int
    mission_level_unknown_data: Pointer[str]
    mission_level_unknown_data_flags_1: int
    mission_level_unknown_data_flags_2: int
    mission_level_unknown_data_flags_3: int
    mission_level_unknown_data_flags_4: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
