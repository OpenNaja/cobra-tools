from generated.formats.enumnamer.compounds.EnumnamerRoot import EnumnamerRoot
from modules.formats.BaseFormat import MemStructLoader


class EnumnamerLoader(MemStructLoader):
	target_class = EnumnamerRoot
	extension = ".enumnamer"
