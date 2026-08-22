from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class FootPlantActivitySmoothTransitionData(MemStruct):

	__name__ = 'FootPlantActivitySmoothTransitionData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.weight = name_type_map['FloatInputData'](self.context, 0, None)
		self.rotation_no_i_k_weight = name_type_map['FloatInputData'](self.context, 0, None)
		self.unknown = name_type_map['Uint64'](self.context, 0, None)
		self.curve = name_type_map['Pointer'](self.context, 0, name_type_map['CurveData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'weight', name_type_map['FloatInputData'], (0, None), (False, None), (None, None)
		yield 'rotation_no_i_k_weight', name_type_map['FloatInputData'], (0, None), (False, None), (None, None)
		yield 'unknown', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'curve', name_type_map['Pointer'], (0, name_type_map['CurveData']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'weight', name_type_map['FloatInputData'], (0, None), (False, None)
		yield 'rotation_no_i_k_weight', name_type_map['FloatInputData'], (0, None), (False, None)
		yield 'unknown', name_type_map['Uint64'], (0, None), (False, None)
		yield 'curve', name_type_map['Pointer'], (0, name_type_map['CurveData']), (False, None)
