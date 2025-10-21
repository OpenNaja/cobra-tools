from generated.formats.chapterdata.compounds.ChapterDataInfo import ChapterDataInfo
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ChapterData(MemStruct):
    chapter_data_name: Pointer[str]
    chapter_data_flags: int
    chapter_data_info_list: ArrayPointer[ChapterDataInfo]
    chapter_data_info_count: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
