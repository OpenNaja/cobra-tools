from generated.formats.trackedridecar.compounds.TrackedRideCarRoot import TrackedRideCarRoot
from modules.formats.BaseFormat import MimeVersionedLoader


class TrackedRideCarLoader(MimeVersionedLoader):
	target_class = TrackedRideCarRoot
	extension = ".trackedridecar"
