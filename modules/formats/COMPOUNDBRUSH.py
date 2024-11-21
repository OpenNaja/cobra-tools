from generated.formats.compoundbrush.structs.CompoundBrushRoot import CompoundBrushRoot
from modules.formats.BaseFormat import MemStructLoader

class CompoundBrush(MemStructLoader):
	target_class = CompoundBrushRoot
	extension = ".compoundbrush"
