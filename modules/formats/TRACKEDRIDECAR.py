from generated.formats.trackedridecar.compound.TrackedRideCarRoot import TrackedRideCarRoot
from modules.formats.BaseFormat import MemStructLoader


class TrackedRideCarLoader(MemStructLoader):
	target_class = TrackedRideCarRoot
	extension = ".trackedridecar"
