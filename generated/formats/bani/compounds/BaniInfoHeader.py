from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bani.imports import name_type_map


class BaniInfoHeader(BaseStruct):

	"""
	Custom header struct
	includes fragments but none of the 3 data buffers
	"""

	__name__ = 'BaniInfoHeader'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 'BANI'
		self.magic = Array(self.context, 0, None, (0,), name_type_map['Byte'])

		# name of the banis file buffer
		self.banis_name = name_type_map['ZString'](self.context, 0, None)
		self.data = name_type_map['BaniRoot'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'magic', Array, (0, None, (4,), name_type_map['Byte']), (False, None), (None, None)
		yield 'banis_name', name_type_map['ZString'], (0, None), (False, None), (None, None)
		yield 'data', name_type_map['BaniRoot'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'magic', Array, (0, None, (4,), name_type_map['Byte']), (False, None)
		yield 'banis_name', name_type_map['ZString'], (0, None), (False, None)
		yield 'data', name_type_map['BaniRoot'], (0, None), (False, None)
