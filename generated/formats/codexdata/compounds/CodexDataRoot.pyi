from generated.formats.codexdata.compounds.CodexChapter import CodexChapter
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class CodexDataRoot(MemStruct):
    codex_data_list: ArrayPointer[CodexChapter]
    codex_data_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
