from generated.base_struct import BaseStruct
from generated.formats.ms2.imports import name_type_map


class ZerosPadding(BaseStruct):

	"""
	1 bit per bone, padded to 8 bytes, all 00
	"""

	__name__ = 'ZerosPadding'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.padding_0 = name_type_map['Uint64'](self.context, 0, None)

		# 128 still has 16 bytes
		self.padding_1 = name_type_map['Uint64'](self.context, 0, None)

		# 129 is the first with 24 bytes
		self.padding_2 = name_type_map['Uint64'](self.context, 0, None)
		self.padding_3 = name_type_map['Uint64'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'padding_0', name_type_map['Uint64'], (0, None), (False, None), (None, True)
		yield 'padding_1', name_type_map['Uint64'], (0, None), (False, None), (None, True)
		yield 'padding_2', name_type_map['Uint64'], (0, None), (False, None), (None, True)
		yield 'padding_3', name_type_map['Uint64'], (0, None), (False, None), (None, True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if 0 < instance.arg:
			yield 'padding_0', name_type_map['Uint64'], (0, None), (False, None)
		if 64 < instance.arg:
			yield 'padding_1', name_type_map['Uint64'], (0, None), (False, None)
		if 128 < instance.arg:
			yield 'padding_2', name_type_map['Uint64'], (0, None), (False, None)
		if 192 < instance.arg:
			yield 'padding_3', name_type_map['Uint64'], (0, None), (False, None)
