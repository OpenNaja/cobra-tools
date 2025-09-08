# START_GLOBALS
import logging
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.motiongraph.imports import name_type_map

# END_GLOBALS


class Activity(MemStruct):

	"""
	48 bytes
	"""

# START_CLASS

	def get_ptr_template(self, prop):
		"""Returns the appropriate template for a pointer named 'prop', if exists.
		Must be overwritten in subclass"""
		if prop == "data":
			activity = self.data_type.data
			key = f"{activity}Data"
			try:
				return name_type_map[key]
			except KeyError:
				logging.debug(f"Motiongraph.{activity} is not supported")
