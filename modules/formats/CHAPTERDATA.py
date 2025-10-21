from generated.formats.chapterdata.structs.ChapterDataRoot import ChapterDataRoot
from modules.formats.BaseFormat import MemStructLoader


class ChapterDataLoader(MemStructLoader):
    target_class = ChapterDataRoot
    extension = ".chapterdata"
