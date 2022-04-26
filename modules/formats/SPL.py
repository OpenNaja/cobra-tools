from generated.formats.spl.compound.SplRoot import SplRoot
from modules.formats.BaseFormat import MemStructLoader


class SplineLoader(MemStructLoader):
	extension = ".spl"
	target_class = SplRoot

