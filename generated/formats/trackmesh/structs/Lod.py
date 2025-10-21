from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackmesh.imports import name_type_map


class Lod(MemStruct):

	"""
	PC : 16 bytes
	PC2: 20 bytes
	"""

	__name__ = 'Lod'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.a = name_type_map['Uint'](self.context, 0, None)
		self.b = name_type_map['Uint'](self.context, 0, None)
		self.c = name_type_map['Uint'](self.context, 0, None)
		self.distance = name_type_map['Float'](self.context, 0, None)
		self.e = name_type_map['Uint'].from_value(1)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'a', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'b', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'c', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'distance', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'e', name_type_map['Uint'], (0, None), (False, 1), (lambda context: context.is_pc_2, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'a', name_type_map['Uint'], (0, None), (False, None)
		yield 'b', name_type_map['Uint'], (0, None), (False, None)
		yield 'c', name_type_map['Uint'], (0, None), (False, None)
		yield 'distance', name_type_map['Float'], (0, None), (False, None)
		if instance.context.is_pc_2:
			yield 'e', name_type_map['Uint'], (0, None), (False, 1)
