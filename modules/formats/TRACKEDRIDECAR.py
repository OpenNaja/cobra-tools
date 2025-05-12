from generated.formats.trackedridecar.compounds.TrackedRideCarRoot import TrackedRideCarRoot
from modules.formats.BaseFormat import MemStructLoader


class TrackedRideCarLoader(MemStructLoader):
	target_class = TrackedRideCarRoot
	extension = ".trackedridecar"

	def collect(self):
		super(TrackedRideCarLoader, self).collect()
		print(self.header.unk_name)