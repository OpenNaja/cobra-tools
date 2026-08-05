from generated.formats.motiongraphvars.structs.MotiongraphVarsRoot import MotiongraphVarsRoot
from modules.formats.BaseFormat import MemStructLoader


class MotiongraphvarsLoader(MemStructLoader):
	target_class = MotiongraphVarsRoot
	extension = ".motiongraphvars"
