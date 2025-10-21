from generated.formats.enumnamer.structs.EnumnamerRoot import EnumnamerRoot
from modules.formats.BaseFormat import MemStructLoader


class MotiongraphvarsLoader(MemStructLoader):
	# probably same layout
	target_class = EnumnamerRoot
	extension = ".motiongraphvars"
