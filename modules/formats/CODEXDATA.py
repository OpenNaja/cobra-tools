from generated.formats.codexdata.compounds.CodexDataRoot import CodexDataRoot
from modules.formats.BaseFormat import MemStructLoader


class CodexDataLoader(MemStructLoader):
    target_class = CodexDataRoot
    extension = ".codexdata"
