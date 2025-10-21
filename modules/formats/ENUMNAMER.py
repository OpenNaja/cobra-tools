from generated.formats.enumnamer.structs.EnumnamerRoot import EnumnamerRoot
from modules.formats.BaseFormat import MemStructLoader


class EnumnamerLoader(MemStructLoader):
	target_class = EnumnamerRoot
	extension = ".enumnamer"
