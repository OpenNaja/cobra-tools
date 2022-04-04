# START_GLOBALS

from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.motiongraph.compound.AnimationActivityData
import generated.formats.motiongraph.compound.FootPlantActivityData
import generated.formats.motiongraph.compound.DataStreamProducerActivityData
import generated.formats.motiongraph.compound.SelectActivityActivityData
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer

# END_GLOBALS


class MRFMember0(MemStruct):

	"""
	48 bytes
	"""

# START_CLASS

	def get_ptr_template(self, prop):
		"""Returns the appropriate template for a pointer named 'prop', if exists.
		Must be overwritten in subclass"""
		# print(f"get_ptr_template MRFMember0")
		if prop == "ptr":
			if self.data_type.data == "AnimationActivity":
				# print(f"data_type {self.data_type.data}")
				return generated.formats.motiongraph.compound.AnimationActivityData.AnimationActivityData
			if self.data_type.data == "FootPlantActivity":
				# print(f"data_type {self.data_type.data}")
				return generated.formats.motiongraph.compound.FootPlantActivityData.FootPlantActivityData
			if self.data_type.data == "DataStreamProducerActivity":
				# print(f"data_type {self.data_type.data}")
				return generated.formats.motiongraph.compound.DataStreamProducerActivityData.DataStreamProducerActivityData
			if self.data_type.data == "SelectActivityActivity":
				# print(f"data_type {self.data_type.data}")
				return generated.formats.motiongraph.compound.SelectActivityActivityData.SelectActivityActivityData
