from generated.formats.trackelement.structs.TrackElementRoot import TrackElementRoot
from modules.formats.BaseFormat import MemStructLoader


class TrackElementLoader(MemStructLoader):
	extension = ".trackelement"
	target_class = TrackElementRoot

