from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.trackelement.structs.TrackElementData import TrackElementData


class TrackElementRoot(MemStruct):
    track_data: ArrayPointer[TrackElementData]
    track_data_count: int
    visual_prefab_name: Pointer[str]
    support_prefab_name: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
