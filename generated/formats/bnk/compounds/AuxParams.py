from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class AuxParams(BaseStruct):

	__name__ = 'AuxParams'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.by_bit_vector = name_type_map['AuxBitfield'](self.context, 0, None)
		self.aux = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.reflections_aux_bus = name_type_map['Uint'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'by_bit_vector', name_type_map['AuxBitfield'], (0, None), (False, None), (None, None)
		yield 'aux', Array, (0, None, (4,), name_type_map['Uint']), (False, None), (None, True)
		yield 'reflections_aux_bus', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'by_bit_vector', name_type_map['AuxBitfield'], (0, None), (False, None)
		if instance.by_bit_vector.b_has_aux:
			yield 'aux', Array, (0, None, (4,), name_type_map['Uint']), (False, None)
		yield 'reflections_aux_bus', name_type_map['Uint'], (0, None), (False, None)
