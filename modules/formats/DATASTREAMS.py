from generated.formats.datastreams.structs.DataStreamsRoot import DataStreamsRoot
from modules.formats.BaseFormat import MemStructLoader


class DataStreamsLoader(MemStructLoader):
	target_class = DataStreamsRoot
	extension = ".datastreams"
