from generated.formats.helpnodedata.compounds.HelpNodeDataHeader import HelpNodeDataHeader
from modules.formats.BaseFormat import MemStructLoader


class HelpNodeDataLoader(MemStructLoader):
	extension = ".helpnodedata"
	target_class = HelpNodeDataHeader
