from generated.formats.lut.compounds.LutHeader import LutHeader
from modules.formats.BaseFormat import MemStructLoader


class LutLoader(MemStructLoader):
	extension = ".lut"
	target_class = LutHeader
