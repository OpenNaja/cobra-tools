from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer
from generated.formats.wmeta.structs.EventEntry import EventEntry


class BnkMetaNew(MemStruct):
    hash: int
    padding: int
    type_name: Pointer[str]
    events: ArrayPointer[EventEntry]
    events_count: int
    hash: int
    flag: int
    unk_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
