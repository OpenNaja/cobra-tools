from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.ovl_base.structs.Pointer import Pointer


class ChapterDataInfo(MemStruct):
    chapter_data_into_str_1: Pointer[str]
    chapter_data_into_str_2: Pointer[str]
    chapter_data_into_str_3: Pointer[str]
    chapter_data_into_str_4: Pointer[str]
    chapter_data_into_str_5: Pointer[str]

    def __init__(self, context: object, arg: int = 0, template: object = None, set_default: bool = True) -> None: ...
