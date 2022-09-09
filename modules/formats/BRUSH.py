from generated.formats.brush.compounds.BrushRoot import BrushRoot
from modules.formats.BaseFormat import MemStructLoader


class BrushLoader(MemStructLoader):
	extension = ".brush"
	target_class = BrushRoot

