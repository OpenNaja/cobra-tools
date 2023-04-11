from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class ManisRoot(BaseStruct):

	"""
	24 bytes for DLA, ZTUAC, PC, JWE1, old PZ
	32 bytes for PZ1.6+, JWE2
	"""

	__name__ = 'ManisRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# seemingly related to the names of mani files stripped from their prefix, but usually slightly smaller than what is actually needed
		self.names_size = name_type_map['Ushort'](self.context, 0, None)
		self.hash_block_size = name_type_map['Ushort'](self.context, 0, None)
		self.zero_0 = name_type_map['Uint'](self.context, 0, None)
		self.zero_1 = name_type_map['Uint64'](self.context, 0, None)
		self.zero_2 = name_type_map['Uint64'](self.context, 0, None)
		self.zero_3 = name_type_map['Uint64'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'names_size', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'hash_block_size', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'zero_0', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'zero_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'zero_3', name_type_map['Uint64'], (0, None), (False, None), (lambda context: context.version >= 260, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'names_size', name_type_map['Ushort'], (0, None), (False, None)
		yield 'hash_block_size', name_type_map['Ushort'], (0, None), (False, None)
		yield 'zero_0', name_type_map['Uint'], (0, None), (False, None)
		yield 'zero_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'zero_2', name_type_map['Uint64'], (0, None), (False, None)
		if instance.context.version >= 260:
			yield 'zero_3', name_type_map['Uint64'], (0, None), (False, None)
