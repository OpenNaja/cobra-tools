from generated.context import ContextReference
from generated.formats.tex.enum.DdsType import DdsType
from generated.formats.tex.enum.DdsTypeCoaster import DdsTypeCoaster


class TexHeader:

	"""
	ZTUAC, PC: 24 bytes, with 1 pointer
	JWE, PZ, JWE2: 40 bytes, with 2 pointers
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# ?
		self.zero_0 = 0

		# ?
		self.zero_1 = 0

		# 8 bytes, all 0
		self.ptr_0 = 0

		# 8 bytes, all 0
		self.ptr_1 = 0

		# flag, not direct index into DDS enum
		self.compression_type = DdsType()

		# flag, not direct index into DDS enum
		self.compression_type = DdsTypeCoaster()

		# 0 or 1
		self.one_0 = 0

		# amount of files combined in this texture, usually 1 or 2, 3 for JWE2 rex
		self.stream_count = 0

		# usually as above
		self.stream_count_repeat = 0

		# 0
		self.pad = 0
		self.set_defaults()

	def set_defaults(self):
		self.zero_0 = 0
		if not (self.context.version < 19):
			self.zero_1 = 0
		self.ptr_0 = 0
		if not (self.context.version < 19):
			self.ptr_1 = 0
		if not (self.context.version < 19):
			self.compression_type = DdsType()
		if self.context.version < 19:
			self.compression_type = DdsTypeCoaster()
		self.one_0 = 0
		self.stream_count = 0
		self.stream_count_repeat = 0
		self.pad = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.zero_0 = stream.read_uint64()
		if not (self.context.version < 19):
			self.zero_1 = stream.read_uint64()
		self.ptr_0 = stream.read_uint64()
		if not (self.context.version < 19):
			self.ptr_1 = stream.read_uint64()
			self.compression_type = DdsType(stream.read_ubyte())
		if self.context.version < 19:
			self.compression_type = DdsTypeCoaster(stream.read_ubyte())
		self.one_0 = stream.read_ubyte()
		self.stream_count = stream.read_ubyte()
		self.stream_count_repeat = stream.read_ubyte()
		self.pad = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.zero_0)
		if not (self.context.version < 19):
			stream.write_uint64(self.zero_1)
		stream.write_uint64(self.ptr_0)
		if not (self.context.version < 19):
			stream.write_uint64(self.ptr_1)
			stream.write_ubyte(self.compression_type.value)
		if self.context.version < 19:
			stream.write_ubyte(self.compression_type.value)
		stream.write_ubyte(self.one_0)
		stream.write_ubyte(self.stream_count)
		stream.write_ubyte(self.stream_count_repeat)
		stream.write_uint(self.pad)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'TexHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zero_0 = {self.zero_0.__repr__()}'
		s += f'\n	* zero_1 = {self.zero_1.__repr__()}'
		s += f'\n	* ptr_0 = {self.ptr_0.__repr__()}'
		s += f'\n	* ptr_1 = {self.ptr_1.__repr__()}'
		s += f'\n	* compression_type = {self.compression_type.__repr__()}'
		s += f'\n	* one_0 = {self.one_0.__repr__()}'
		s += f'\n	* stream_count = {self.stream_count.__repr__()}'
		s += f'\n	* stream_count_repeat = {self.stream_count_repeat.__repr__()}'
		s += f'\n	* pad = {self.pad.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
