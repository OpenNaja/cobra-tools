from generated.formats.animalresearch.compounds.ResearchRoot import ResearchRoot
from generated.formats.animalresearch.compounds.ResearchStartRoot import ResearchStartRoot
from modules.formats.BaseFormat import MemStructLoader


class AnimalresearchunlockssettingsLoader(MemStructLoader):
	target_class = ResearchRoot
	extension = ".animalresearchunlockssettings"

	def collect(self):
		super().collect()
		# print(self.header)

	def prep(self):
		# avoid generating pointers for these
		for level in self.header.levels.data:
			if not level.next_level_count:
				level.next_levels.data = None
			if not level.children_count:
				level.children.data = None

	def create(self):
		self.create_root_entry()
		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		# print(self.header)
		self.prep()
		self.header.write_ptrs(self, self.root_ptr, self.file_entry.pool_type)


class AnimalresearchstartunlockedssettingsLoader(MemStructLoader):
	target_class = ResearchStartRoot
	extension = ".animalresearchstartunlockedsettings"
