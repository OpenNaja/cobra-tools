from generated.formats.techtree.compounds.TechTreeRoot import TechTreeRoot
from modules.formats.BaseFormat import MemStructLoader

class TechTreeLoader(MemStructLoader):
	target_class = TechTreeRoot
	extension = ".techtree"