from generated.formats.trackedridecar.compounds.TrackedRideCarRoot import TrackedRideCarRoot
from modules.formats.BaseFormat import MemStructLoader


class TrackedRideCarLoader(MemStructLoader):
	target_class = TrackedRideCarRoot
	extension = ".trackedridecar"
