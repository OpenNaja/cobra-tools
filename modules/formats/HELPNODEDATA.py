from generated.formats.helpnodedata.structs.HelpNodeDataHeader import HelpNodeDataHeader
from modules.formats.BaseFormat import MemStructLoader


class HelpNodeDataLoader(MemStructLoader):
	extension = ".helpnodedata"
	target_class = HelpNodeDataHeader
