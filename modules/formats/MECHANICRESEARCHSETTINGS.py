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

	def create(self, file_path):
		self.create_root_entry()
		self.header = self.target_class.from_xml_file(file_path, self.ovl.context)
		self.prep()
		self.write_memory_data()


