from generated.base_struct import BaseStruct
from generated.formats.bani.imports import name_type_map


class BoneInfo(BaseStruct):

	"""
	PC2: 2 bytes
	"""

	__name__ = 'BoneInfo'

	allow_np = True

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.index = name_type_map['Ubyte'](self.context, 0, None)
		self.flag = name_type_map['Ubyte'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'index', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'flag', name_type_map['Ubyte'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'index', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'flag', name_type_map['Ubyte'], (0, None), (False, None)
