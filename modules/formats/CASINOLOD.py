from generated.formats.casinolod.structs.CasinoLodRoot import CasinoLodRoot
from modules.formats.BaseFormat import MemStructLoader


class CasinoLodLoader(MemStructLoader):
	target_class = CasinoLodRoot
	extension = ".casinolod"
