from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class AdvSettingsParams(BaseStruct):

	__name__ = 'AdvSettingsParams'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.by_bit_vector = name_type_map['Ubyte'](self.context, 0, None)
		self.e_virtual_queue_behavior = name_type_map['Ubyte'](self.context, 0, None)
		self.u_16_max_num_instance = name_type_map['Ushort'](self.context, 0, None)
		self.e_below_threshold_behavior = name_type_map['Ubyte'](self.context, 0, None)
		self.by_bit_vector = name_type_map['Ubyte'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'by_bit_vector', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'e_virtual_queue_behavior', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'u_16_max_num_instance', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'e_below_threshold_behavior', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'by_bit_vector', name_type_map['Ubyte'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'by_bit_vector', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'e_virtual_queue_behavior', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'u_16_max_num_instance', name_type_map['Ushort'], (0, None), (False, None)
		yield 'e_below_threshold_behavior', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'by_bit_vector', name_type_map['Ubyte'], (0, None), (False, None)
