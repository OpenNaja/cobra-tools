from generated.formats.specdef.compounds.SpecdefRoot import SpecdefRoot
from modules.formats.BaseFormat import MemStructLoader


class SpecdefLoader(MemStructLoader):
	target_class = SpecdefRoot
	extension = ".specdef"
