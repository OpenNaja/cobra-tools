from generated.formats.datastreams.compounds.DataStreamsRoot import DataStreamsRoot
from modules.formats.BaseFormat import MemStructLoader


class DataStreamsLoader(MemStructLoader):
	target_class = DataStreamsRoot
	extension = ".datastreams"
