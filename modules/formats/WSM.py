from generated.formats.wsm.structs.WsmHeader import WsmHeader
from modules.formats.BaseFormat import MemStructLoader


class WsmLoader(MemStructLoader):
	extension = ".wsm"
	target_class = WsmHeader

