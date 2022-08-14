from generated.formats.xmlconfig.compounds.XmlconfigRoot import XmlconfigRoot
from modules.formats.BaseFormat import MemStructLoader


class XmlconfigLoader(MemStructLoader):
	extension = ".xmlconfig"
	target_class = XmlconfigRoot

