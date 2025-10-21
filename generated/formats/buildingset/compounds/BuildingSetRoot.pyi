from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class BuildingSetRoot(MemStruct):
    set_id_name: Pointer[str]
    set_count_or_type: int
    unk_1_found_as_0: int
    unk_2_found_as_0: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
