from generated.formats.fmvdesc.structs.FMVDescRoot import FMVDescRoot
from modules.formats.BaseFormat import MemStructLoader


class FMVDescLoader(MemStructLoader):
	extension = ".fmvdesc"
	target_class = FMVDescRoot

