from generated.formats.ppuipkg.structs.PPUIPKGRoot import PPUIPKGRoot
from modules.formats.BaseFormat import MemStructLoader


class PPUIPKGLoader(MemStructLoader):
	extension = ".ppuipkg"
	target_class = PPUIPKGRoot

