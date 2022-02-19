from generated.context import ContextReference


class SizedStrData:

	"""
	24 bytes for DLA, ZTUAC, PC, JWE1, old PZ
	32 bytes for PZ1.6+, JWE2
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# seemingly related to the names of mani files stripped from their prefix, but usually slightly smaller than what is actually needed
		self.names_size = 0
		self.hash_block_size = 0
		self.zero_0 = 0

		# haven't seen this one actually used, may be wrong
		self.count = 0
		self.zero_1 = 0
		self.zero_2 = 0
		self.set_defaults()

	def set_defaults(self):
		self.names_size = 0
		self.hash_block_size = 0
		self.zero_0 = 0
		self.count = 0
		self.zero_1 = 0
		if self.context.version >= 20:
			self.zero_2 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.names_size = stream.read_ushort()
		self.hash_block_size = stream.read_ushort()
		self.zero_0 = stream.read_uint64()
		self.count = stream.read_uint()
		self.zero_1 = stream.read_uint64()
		if self.context.version >= 20:
			self.zero_2 = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_ushort(self.names_size)
		stream.write_ushort(self.hash_block_size)
		stream.write_uint64(self.zero_0)
		stream.write_uint(self.count)
		stream.write_uint64(self.zero_1)
		if self.context.version >= 20:
			stream.write_uint64(self.zero_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'SizedStrData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* names_size = {self.names_size.__repr__()}'
		s += f'\n	* hash_block_size = {self.hash_block_size.__repr__()}'
		s += f'\n	* zero_0 = {self.zero_0.__repr__()}'
		s += f'\n	* count = {self.count.__repr__()}'
		s += f'\n	* zero_1 = {self.zero_1.__repr__()}'
		s += f'\n	* zero_2 = {self.zero_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
