from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.ovl_base.structs.ZStringList import ZStringList


class TrackMeshElement(MemStruct):
    element_id: Pointer[str]
    objects_list: Pointer[ZStringList]
    objects_list_count: int
    flanges: Pointer[ZStringList]
    flanges_count: int
    start_1: Pointer[ZStringList]
    start_1_count: int
    start_2: Pointer[ZStringList]
    start_2_count: int
    start_3: Pointer[ZStringList]
    start_3_count: int
    stop_1: Pointer[ZStringList]
    stop_1_count: int
    stop_2: Pointer[ZStringList]
    stop_2_count: int
    unknown_1: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
