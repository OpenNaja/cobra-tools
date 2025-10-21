from generated.formats.specdef.structs.SpecdefRoot import SpecdefRoot
from modules.formats.BaseFormat import MemStructLoader


class SpecdefLoader(MemStructLoader):
	target_class = SpecdefRoot
	extension = ".specdef"

	def extract(self, out_dir):
		print(self.header)
		return super(SpecdefLoader, self).extract(out_dir)
