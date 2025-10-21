from generated.formats.brush.structs.BrushRoot import BrushRoot
from modules.formats.BaseFormat import MemStructLoader


class BrushLoader(MemStructLoader):
	extension = ".brush"
	target_class = BrushRoot

