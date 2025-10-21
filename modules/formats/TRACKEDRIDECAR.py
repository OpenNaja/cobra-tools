from generated.formats.trackedridecar.structs.TrackedRideCarRoot import TrackedRideCarRoot
from modules.formats.BaseFormat import MimeVersionedLoader


class TrackedRideCarLoader(MimeVersionedLoader):
	target_class = TrackedRideCarRoot
	extension = ".trackedridecar"
