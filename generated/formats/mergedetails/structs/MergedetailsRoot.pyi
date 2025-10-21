from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.ovl_base.structs.ZStringList import ZStringList


class MergedetailsRoot(MemStruct):
    merge_names: Pointer[ZStringList]
    unk_names: Pointer[ZStringList]
    zero_1: int
    queries: Pointer[ZStringList]
    field_name: Pointer[str]
    count_0: int
    count_1: int
    count_2: int
    count_3: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
