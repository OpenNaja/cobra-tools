from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.landscape.imports import name_type_map


class Buffer0(BaseStruct):

	__name__ = 'Buffer0'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.names = name_type_map['ZStringBuffer'](self.context, self.arg.name_buffer_size, None)
		self.names_padding = name_type_map['PadAlign'](self.context, 8, self.names)
		self.floats = Array(self.context, 0, None, (0,), name_type_map['Float'])
		self.stuff = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.name_indices = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'names', name_type_map['ZStringBuffer'], (None, None), (False, None), (None, None)
		yield 'names_padding', name_type_map['PadAlign'], (8, None), (False, None), (None, None)
		yield 'floats', Array, (0, None, (14,), name_type_map['Float']), (False, None), (None, None)
		yield 'stuff', Array, (0, None, (30,), name_type_map['Uint']), (False, None), (None, None)
		yield 'name_indices', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'names', name_type_map['ZStringBuffer'], (instance.arg.name_buffer_size, None), (False, None)
		yield 'names_padding', name_type_map['PadAlign'], (8, instance.names), (False, None)
		yield 'floats', Array, (0, None, (14,), name_type_map['Float']), (False, None)
		yield 'stuff', Array, (0, None, (30,), name_type_map['Uint']), (False, None)
		yield 'name_indices', Array, (0, None, (instance.arg.things_count,), name_type_map['Uint']), (False, None)
