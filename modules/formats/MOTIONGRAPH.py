from generated.formats.motiongraph.compounds.MotiongraphHeader import MotiongraphHeader
from modules.formats.BaseFormat import MemStructLoader


class MotiongraphLoader(MemStructLoader):
	target_class = MotiongraphHeader
	extension = ".motiongraph"

	def collect(self):
		if self.ovl.version >= 19:
			super().collect()
