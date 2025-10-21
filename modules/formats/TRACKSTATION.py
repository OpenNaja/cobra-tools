from generated.formats.trackstation.structs.TrackStationRoot import TrackStationRoot
from modules.formats.BaseFormat import MemStructLoader


class TrackStationLoader(MemStructLoader):
	extension = ".trackstation"
	target_class = TrackStationRoot

