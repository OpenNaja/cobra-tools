from generated.formats.trackelement.compounds.TrackElementRoot import TrackElementRoot
from modules.formats.BaseFormat import MemStructLoader


class TrackElementLoader(MemStructLoader):
	extension = ".trackelement"
	target_class = TrackElementRoot

