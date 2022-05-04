from generated.formats.xmlconfig.compound.XmlconfigRoot import XmlconfigRoot
from modules.formats.BaseFormat import MemStructLoader


class XmlconfigLoader(MemStructLoader):
	extension = ".xmlconfig"
	target_class = XmlconfigRoot

