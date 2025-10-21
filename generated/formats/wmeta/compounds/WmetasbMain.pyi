from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.wmeta.compounds.EventEntry import EventEntry
from generated.formats.wmeta.compounds.MediaEntry import MediaEntry


class WmetasbMain(MemStruct):
    hash: int
    unk: int
    block_name: Pointer[str]
    media_name: Pointer[str]
    bnk_name: Pointer[str]
    events: ArrayPointer[EventEntry]
    events_count: int
    hashes: ArrayPointer[int]
    hashes_count: int
    media: ArrayPointer[MediaEntry]
    media_count: int
    unused_2: Pointer[object]
    unused_3: Pointer[object]
    unused_4: Pointer[object]
    unused_5: Pointer[object]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
