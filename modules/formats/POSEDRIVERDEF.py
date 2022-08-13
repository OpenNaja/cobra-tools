from generated.formats.posedriverdef.compounds.PoseDriverDefRoot import PoseDriverDefRoot
from modules.formats.BaseFormat import MemStructLoader


class PosedriverdefLoader(MemStructLoader):
	target_class = PoseDriverDefRoot
	extension = ".posedriverdef"
