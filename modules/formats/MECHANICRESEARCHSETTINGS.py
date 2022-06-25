from generated.formats.mechanicresearch.compound.ResearchRoot import ResearchRoot
#from generated.formats.mechanicresearch.compound.ResearchStartRoot import ResearchStartRoot
from modules.formats.BaseFormat import MemStructLoader


class MechanicresearchsettingsLoader(MemStructLoader):
	target_class = ResearchRoot
	extension = ".mechanicresearchsettings"

	#def collect(self):
	#	super().collect()
		# self.header.debug_ptrs()
		# print(self.header)

	def prep(self):
		# avoid generating pointers for these
		for research in self.header.levels.data:
			if not research.next_research_count:
				research.next_research.data = None
			if not research.children_count:
				research.children.data = None

	def create(self):
		self.create_root_entry()
		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		# print(self.header)
		self.prep()
		self.header.write_ptrs(self, self.root_ptr, self.file_entry.pool_type)


