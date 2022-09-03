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
		# print(f"get_ptr_template Activity")
		if prop == "ptr":
			activity = self.data_type.data
			# print(f"data_type {self.data_type.data}")
			if activity == "AnimationActivity":
				# print(f"data_type {self.data_type.data}")
				return generated.formats.motiongraph.compounds.AnimationActivityData.AnimationActivityData
			elif activity == "FootPlantActivity":
				# print(f"data_type {self.data_type.data}")
				return generated.formats.motiongraph.compounds.FootPlantActivityData.FootPlantActivityData
			elif activity == "DataStreamProducerActivity":
				# print(f"data_type {self.data_type.data}")
				return generated.formats.motiongraph.compounds.DataStreamProducerActivityData.DataStreamProducerActivityData
			elif activity == "SelectActivityActivity":
				# print(f"data_type {self.data_type.data}")
				return generated.formats.motiongraph.compounds.SelectActivityActivityData.SelectActivityActivityData
			else:
				logging.warning(f"Unsupported activity '{activity}'")
