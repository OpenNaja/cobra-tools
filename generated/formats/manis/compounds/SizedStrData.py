from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort


class SizedStrData(BaseStruct):

	"""
	24 bytes for DLA, ZTUAC, PC, JWE1, old PZ
	32 bytes for PZ1.6+, JWFloatCount
	"""

	__name__ = 'SizedStrData'

	_import_path = 'generated.formats.manis.compounds.SizedStrData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# seemingly related to the names of mani files stripped from their prefix, but usually slightly smaller than what is actually needed
		self.names_size = 0
		self.hash_block_size = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.zero_2 = 0
		self.zero_3 = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'names_size', Ushort, (0, None), (False, None)
		yield 'hash_block_size', Ushort, (0, None), (False, None)
		yield 'zero_0', Uint, (0, None), (False, None)
		yield 'zero_1', Uint64, (0, None), (False, None)
		yield 'zero_2', Uint64, (0, None), (False, None)
		if instance.context.version >= 20:
			yield 'zero_3', Uint64, (0, None), (False, None)
