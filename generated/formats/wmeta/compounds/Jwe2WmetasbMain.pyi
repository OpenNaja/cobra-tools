from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer
from generated.formats.wmeta.compounds.EventEntry import EventEntry


class Jwe2WmetasbMain(MemStruct):
    block_name: Pointer[str]
    events: ArrayPointer[EventEntry]
    events_count: int
    hash: int
    unk_1: int
    unk_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
