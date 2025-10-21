from generated.formats.chapterdata.structs.ChapterData import ChapterData
from generated.formats.ovl_base.structs.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ChapterDataRoot(MemStruct):
    chapter_data_type: int
    chapter_data_hidden: int
    chapter_data_id: int
    chapter_data_zero: int
    chapter_data_unused_1: int
    chapter_data_list_1: int
    chapter_data_list_2: int
    chapter_data_list_3: int
    chapter_data_list_4: int
    chapter_data_count_1: int
    chapter_data_count_2: int
    chapter_data_count_3: int
    chapter_data_count_4: int
    chapter_data_list: ArrayPointer[ChapterData]
    chapter_data_count: int
    chapter_data_unused_2: int

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
