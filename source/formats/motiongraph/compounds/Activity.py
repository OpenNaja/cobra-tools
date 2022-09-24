# START_GLOBALS
import logging

import generated.formats.base.basic
import generated.formats.motiongraph.compounds.AnimationActivityData
import generated.formats.motiongraph.compounds.FootPlantActivityData
import generated.formats.motiongraph.compounds.DataStreamProducerActivityData
import generated.formats.motiongraph.compounds.SelectActivityActivityData
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer

# END_GLOBALS


class Activity(MemStruct):

	"""
	48 bytes
	"""

# START_CLASS

	def get_ptr_template(self, prop):
		"""Returns the appropriate template for a pointer named 'prop', if exists.
		Must be overwritten in subclass"""
		if prop == "ptr":
			activity = self.data_type.data
			key = f"motiongraph.compounds.{activity}Data"
			try:
				return Activity._import_map[key]
			except:
				logging.warning(f"Unsupported activity '{activity}'")
