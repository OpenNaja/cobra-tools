from generated.formats.animalresearch.compounds.ResearchRoot import ResearchRoot
from generated.formats.animalresearch.compounds.ResearchStartRoot import ResearchStartRoot
from modules.formats.BaseFormat import MemStructLoader


class AnimalresearchunlockssettingsLoader(MemStructLoader):
	target_class = ResearchRoot
	extension = ".animalresearchunlockssettings"

	def prep(self):
		# avoid generating pointers for these
		for level in self.header.levels.data:
			if not level.next_level_count:
				level.next_levels.data = None
			if not level.children_count:
				level.children.data = None

	def create(self, file_path):
		self.header = self.target_class.from_xml_file(file_path, self.ovl.context)
		self.prep()
		self.write_memory_data()


class AnimalresearchstartunlockedssettingsLoader(MemStructLoader):
	target_class = ResearchStartRoot
	extension = ".animalresearchstartunlockedsettings"
