from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.wmeta.structs.EventEntry import EventEntry
from generated.formats.wmeta.structs.MediaEntry import MediaEntry


class BnkMeta(MemStruct):
    hash: int
    _padding: int
    type_name: Pointer[str]
    bnk_name: Pointer[str]
    file_name: Pointer[str]
    events: ArrayPointer[EventEntry]
    events_count: int
    hashes: ArrayPointer[int]
    hashes_count: int
    media: ArrayPointer[MediaEntry]
    media_count: int
    unused_2: int
    unused_3: int
    unused_4: int
    unused_5: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
