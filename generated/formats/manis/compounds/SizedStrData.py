from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort


class SizedStrData(BaseStruct):

	"""
	24 bytes for DLA, ZTUAC, PC, JWE1, old PZ
	32 bytes for PZ1.6+, JWFloatCount
	"""

	__name__ = SizedStrData

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# seemingly related to the names of mani files stripped from their prefix, but usually slightly smaller than what is actually needed
		self.names_size = 0
		self.hash_block_size = 0
		self.zero_0 = 0

		# haven't seen this one actually used, may be wrong
		self.count = 0
		self.zero_1 = 0
		self.zero_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.names_size = 0
		self.hash_block_size = 0
		self.zero_0 = 0
		self.count = 0
		self.zero_1 = 0
		if self.context.version >= 20:
			self.zero_2 = 0

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.names_size = Ushort.from_stream(stream, instance.context, 0, None)
		instance.hash_block_size = Ushort.from_stream(stream, instance.context, 0, None)
		instance.zero_0 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.count = Uint.from_stream(stream, instance.context, 0, None)
		instance.zero_1 = Uint64.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 20:
			instance.zero_2 = Uint64.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Ushort.to_stream(stream, instance.names_size)
		Ushort.to_stream(stream, instance.hash_block_size)
		Uint64.to_stream(stream, instance.zero_0)
		Uint.to_stream(stream, instance.count)
		Uint64.to_stream(stream, instance.zero_1)
		if instance.context.version >= 20:
			Uint64.to_stream(stream, instance.zero_2)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'names_size', Ushort, (0, None), (False, None)
		yield 'hash_block_size', Ushort, (0, None), (False, None)
		yield 'zero_0', Uint64, (0, None), (False, None)
		yield 'count', Uint, (0, None), (False, None)
		yield 'zero_1', Uint64, (0, None), (False, None)
		if instance.context.version >= 20:
			yield 'zero_2', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'SizedStrData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* names_size = {self.fmt_member(self.names_size, indent+1)}'
		s += f'\n	* hash_block_size = {self.fmt_member(self.hash_block_size, indent+1)}'
		s += f'\n	* zero_0 = {self.fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* count = {self.fmt_member(self.count, indent+1)}'
		s += f'\n	* zero_1 = {self.fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* zero_2 = {self.fmt_member(self.zero_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
