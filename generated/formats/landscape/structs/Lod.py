from generated.base_struct import BaseStruct
from generated.formats.landscape.imports import name_type_map


class Lod(BaseStruct):

	"""
	16 bytes
	"""

	__name__ = 'Lod'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.index = name_type_map['Uint'](self.context, 0, None)
		self.unk = name_type_map['Uint'](self.context, 0, None)
		self.unk_2 = name_type_map['Ushort'](self.context, 0, None)
		self.index_1 = name_type_map['Ushort'](self.context, 0, None)
		self.distance = name_type_map['Float'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'index', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'unk_2', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'index_1', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'distance', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'index', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk', name_type_map['Uint'], (0, None), (False, None)
		yield 'unk_2', name_type_map['Ushort'], (0, None), (False, None)
		yield 'index_1', name_type_map['Ushort'], (0, None), (False, None)
		yield 'distance', name_type_map['Float'], (0, None), (False, None)
