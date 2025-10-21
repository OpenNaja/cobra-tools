from generated.formats.spl.structs.SplRoot import SplRoot
from modules.formats.BaseFormat import MemStructLoader


class SplineLoader(MemStructLoader):
	extension = ".spl"
	target_class = SplRoot

