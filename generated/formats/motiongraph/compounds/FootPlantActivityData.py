from generated.formats.motiongraph.compounds.FloatInputData import FloatInputData
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FootPlantActivityData(MemStruct):

	"""
	48 bytes
	"""

	__name__ = 'FootPlantActivityData'

	_import_key = 'motiongraph.compounds.FootPlantActivityData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.weight = FloatInputData(self.context, 0, None)
		self.rotation_no_i_k_weight = FloatInputData(self.context, 0, None)
		self.sticky_feet_weight = FloatInputData(self.context, 0, None)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('weight', FloatInputData, (0, None), (False, None), None),
		('rotation_no_i_k_weight', FloatInputData, (0, None), (False, None), None),
		('sticky_feet_weight', FloatInputData, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'weight', FloatInputData, (0, None), (False, None)
		yield 'rotation_no_i_k_weight', FloatInputData, (0, None), (False, None)
		yield 'sticky_feet_weight', FloatInputData, (0, None), (False, None)
