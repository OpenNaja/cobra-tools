from generated.formats.mechanicresearch.compounds.ResearchRoot import ResearchRoot
from modules.formats.BaseFormat import MemStructLoader


class MechanicresearchsettingsLoader(MemStructLoader):
	target_class = ResearchRoot
	extension = ".mechanicresearchsettings"

	def prep(self):
		# avoid generating pointers for these
		for research in self.header.levels.data:
			if not research.next_research_count:
				research.next_research.data = None

	def create(self):
		self.create_root_entry()
		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		# print(self.header)
		self.prep()
		self.header.write_ptrs(self, self.root_ptr, self.file_entry.pool_type)


