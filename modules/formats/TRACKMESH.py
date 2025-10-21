from generated.formats.trackmesh.structs.TrackMeshRoot import TrackMeshRoot
from modules.formats.BaseFormat import MemStructLoader


class TrackMeshLoader(MemStructLoader):
	extension = ".trackmesh"
	target_class = TrackMeshRoot

