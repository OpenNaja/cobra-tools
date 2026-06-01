from generated.base_struct import BaseStruct
from generated.formats.landscape.imports import name_type_map


class Pass(BaseStruct):

	"""
	8 bytes
	"""

	__name__ = 'Pass'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.name = name_type_map['NameOffset'](self.context, self.arg, None)
		self.a = name_type_map['Ushort'](self.context, 0, None)
		self.b = name_type_map['Ushort'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'name', name_type_map['NameOffset'], (None, None), (False, None), (None, None)
		yield 'a', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'b', name_type_map['Ushort'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'name', name_type_map['NameOffset'], (instance.arg, None), (False, None)
		yield 'a', name_type_map['Ushort'], (0, None), (False, None)
		yield 'b', name_type_map['Ushort'], (0, None), (False, None)
