from generated.formats.motiongraph.compound.MotiongraphHeader import MotiongraphHeader
from modules.formats.BaseFormat import MemStructLoader


class MotiongraphLoader(MemStructLoader):
	target_class = MotiongraphHeader
	extension = ".motiongraph"

	def rename_content(self, name_tuples):
		self.rename_fragments(name_tuples)
