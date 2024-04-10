from generated.formats.casinolod.compounds.CasinoLodRoot import CasinoLodRoot
from modules.formats.BaseFormat import MemStructLoader


class CasinoLodLoader(MemStructLoader):
	target_class = CasinoLodRoot
	extension = ".casinolod"
