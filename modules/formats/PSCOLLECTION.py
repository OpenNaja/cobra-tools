from generated.formats.pscollection.compound.PscollectionRoot import PscollectionRoot
from modules.formats.BaseFormat import MemStructLoader


class PSCollectionLoader(MemStructLoader):
	extension = ".pscollection"
	target_class = PscollectionRoot
