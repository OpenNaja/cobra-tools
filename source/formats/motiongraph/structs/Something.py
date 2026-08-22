# START_GLOBALS
from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.motiongraph.imports import name_type_map

# END_GLOBALS


class Something(MemStruct):

# START_CLASS

	def get_ptr_template(self, prop):
		if prop != "ptr":
			return None
		if int(self.unk) == 0:
			return name_type_map["MotiongraphVar"]
		if int(self.unk) == 1:
			return name_type_map["MotiongraphResultParam"]
		if int(self.unk) == 2:
			return name_type_map["MotiongraphRangeParams"]
		return None

