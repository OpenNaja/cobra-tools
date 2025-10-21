from generated.formats.techtree.structs.TechTreeRoot import TechTreeRoot
from modules.formats.BaseFormat import MemStructLoader

class TechTreeLoader(MemStructLoader):
	target_class = TechTreeRoot
	extension = ".techtree"