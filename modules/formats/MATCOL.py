from generated.formats.matcol.compounds.MatcolRoot import MatcolRoot
from modules.formats.BaseFormat import MemStructLoader


class MatcolLoader(MemStructLoader):
	target_class = MatcolRoot
	extension = ".materialcollection"
	aliases = (".matcol", )
