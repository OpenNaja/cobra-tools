from generated.formats.animalresearch.compound.ResearchRoot import ResearchRoot
from generated.formats.animalresearch.compound.ResearchStartRoot import ResearchStartRoot
from modules.formats.BaseFormat import MemStructLoader


class AnimalresearchunlockssettingsLoader(MemStructLoader):
	target_class = ResearchRoot
	extension = ".animalresearchunlockssettings"

	def collect(self):
		super().collect()
		# self.header.debug_ptrs()
		print(self.header)

	def create(self):
		self.root_entry = self.create_root_entry(self.file_entry)
		self.header = self.target_class.from_xml_file(self.file_entry.path, self.ovl.context)
		# print(self.header)
		# avoid generating pointers for these
		for level in self.header.levels:
			if not level.next_level_count:
				level.next_levels.data = None
			if not level.children_count:
				level.children.data = None
		self.header.write_ptrs(self, self.ovs, self.root_ptr, self.file_entry.pool_type)


class AnimalresearchstartunlockedssettingsLoader(MemStructLoader):
	target_class = ResearchStartRoot
	extension = ".animalresearchstartunlockedsettings"
