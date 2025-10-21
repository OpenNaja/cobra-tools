from generated.formats.mechanicresearch.structs.NextResearch import NextResearch
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class Research(MemStruct):
    item_name: Pointer[str]
    is_completed: int
    is_entry_level: int
    is_enabled: int
    next_research: Pointer[NextResearch]
    next_research_count: int
    unk_3: int
    unk_4: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
