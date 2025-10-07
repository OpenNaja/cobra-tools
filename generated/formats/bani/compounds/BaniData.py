from generated.formats.bani.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class BaniData(MemStruct):

	"""
	PC2: 16 bytes
	"""

	__name__ = 'BaniData'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = name_type_map['Ushort'](self.context, 0, None)
		self.b = name_type_map['Ushort'](self.context, 0, None)
		self.unk = name_type_map['Float'](self.context, 0, None)
		self.increment = name_type_map['Ushort'](self.context, 0, None)
		self.zero = name_type_map['Ubyte'].from_value(0)
		self.num_bones = name_type_map['Ubyte'](self.context, 0, None)
		self.index_reversed = name_type_map['Uint'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'a', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'b', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'unk', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'increment', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'zero', name_type_map['Ubyte'], (0, None), (False, 0), (None, None)
		yield 'num_bones', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'index_reversed', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', name_type_map['Ushort'], (0, None), (False, None)
		yield 'b', name_type_map['Ushort'], (0, None), (False, None)
		yield 'unk', name_type_map['Float'], (0, None), (False, None)
		yield 'increment', name_type_map['Ushort'], (0, None), (False, None)
		yield 'zero', name_type_map['Ubyte'], (0, None), (False, 0)
		yield 'num_bones', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'index_reversed', name_type_map['Uint'], (0, None), (False, None)
