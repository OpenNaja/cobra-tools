from generated.formats.physmat.compounds.PhysmatRoot import PhysmatRoot
from modules.formats.BaseFormat import MemStructLoader


class PhysmatLoader(MemStructLoader):
	target_class = PhysmatRoot
	extension = ".physmat"
