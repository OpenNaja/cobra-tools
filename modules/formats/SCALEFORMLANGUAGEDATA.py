from generated.formats.scaleformlanguagedata.compound.ScaleformlanguagedataRoot import ScaleformlanguagedataRoot
from modules.formats.BaseFormat import MemStructLoader


class ScaleformLoader(MemStructLoader):
	extension = ".scaleformlanguagedata"
	target_class = ScaleformlanguagedataRoot
