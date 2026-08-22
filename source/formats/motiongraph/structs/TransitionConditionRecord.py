# START_GLOBALS
from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct
# END_GLOBALS


class TransitionConditionRecord(MemStruct):

	"""72-byte transition-local condition record."""

# START_CLASS

	def get_ptr_template(self, prop):
		if prop == "curve":
			return name_type_map["CurveData"]
