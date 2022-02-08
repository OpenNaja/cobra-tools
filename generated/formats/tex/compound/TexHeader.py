from generated.context import ContextReference
from generated.formats.tex.enum.DdsType import DdsType
from generated.formats.tex.enum.DdsTypeCoaster import DdsTypeCoaster


class TexHeader:

	"""
	DLA: 24 bytes, no pointers
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
		self.zero_0 = 0
		self.zero_0 = 0
		self.zero_1 = 0

		# 8 bytes, all 0
		self.ptr_0 = 0

		# 8 bytes, all 0
		self.ptr_1 = 0
		self.compression_type = DdsType()
		self.compression_type = DdsTypeCoaster()

		# 0 or 1
		self.one_0 = 0
		self.num_mips = 0
		self.width = 0
		self.height = 0

		# amount of files combined in this texture, usually 1 or 2, 3 for JWE2 rex
		self.stream_count = 0

		# usually as above
		self.stream_count_repeat = 0

		# 0
		self.pad = 0
		self.pad_dla = 0
		self.set_defaults()

	def set_defaults(self):
		if self.context.version <= 15:
			self.zero_0 = 0
		if self.context.version >= 17:
			self.zero_0 = 0
		if self.context.version >= 19:
			self.zero_1 = 0
		if self.context.version >= 17:
			self.ptr_0 = 0
		if self.context.version >= 19:
			self.ptr_1 = 0
		if not (self.context.version < 19):
			self.compression_type = DdsType()
		if self.context.version < 19:
			self.compression_type = DdsTypeCoaster()
		self.one_0 = 0
		if self.context.version <= 15:
			self.num_mips = 0
		if self.context.version <= 15:
			self.width = 0
		if self.context.version <= 15:
			self.height = 0
		if self.context.version >= 17:
			self.stream_count = 0
		if self.context.version >= 17:
			self.stream_count_repeat = 0
		self.pad = 0
		if self.context.version <= 15:
			self.pad_dla = 0

	def read(self, stream):
		self.io_start = stream.tell()
		if self.context.version <= 15:
			self.zero_0 = stream.read_uint()
		if self.context.version >= 17:
			self.zero_0 = stream.read_uint64()
		if self.context.version >= 19:
			self.zero_1 = stream.read_uint64()
		if self.context.version >= 17:
			self.ptr_0 = stream.read_uint64()
		if self.context.version >= 19:
			self.ptr_1 = stream.read_uint64()
		if not (self.context.version < 19):
			self.compression_type = DdsType(stream.read_ubyte())
		if self.context.version < 19:
			self.compression_type = DdsTypeCoaster(stream.read_ubyte())
		self.one_0 = stream.read_ubyte()
		if self.context.version <= 15:
			self.num_mips = stream.read_ushort()
			self.width = stream.read_ushort()
		if self.context.version <= 15:
			self.height = stream.read_ushort()
		if self.context.version >= 17:
			self.stream_count = stream.read_ubyte()
			self.stream_count_repeat = stream.read_ubyte()
		self.pad = stream.read_uint()
		if self.context.version <= 15:
			self.pad_dla = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		if self.context.version <= 15:
			stream.write_uint(self.zero_0)
		if self.context.version >= 17:
			stream.write_uint64(self.zero_0)
		if self.context.version >= 19:
			stream.write_uint64(self.zero_1)
		if self.context.version >= 17:
			stream.write_uint64(self.ptr_0)
		if self.context.version >= 19:
			stream.write_uint64(self.ptr_1)
		if not (self.context.version < 19):
			stream.write_ubyte(self.compression_type.value)
		if self.context.version < 19:
			stream.write_ubyte(self.compression_type.value)
		stream.write_ubyte(self.one_0)
		if self.context.version <= 15:
			stream.write_ushort(self.num_mips)
			stream.write_ushort(self.width)
		if self.context.version <= 15:
			stream.write_ushort(self.height)
		if self.context.version >= 17:
			stream.write_ubyte(self.stream_count)
			stream.write_ubyte(self.stream_count_repeat)
		stream.write_uint(self.pad)
		if self.context.version <= 15:
			stream.write_uint64(self.pad_dla)

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
		s += f'\n	* num_mips = {self.num_mips.__repr__()}'
		s += f'\n	* width = {self.width.__repr__()}'
		s += f'\n	* height = {self.height.__repr__()}'
		s += f'\n	* stream_count = {self.stream_count.__repr__()}'
		s += f'\n	* stream_count_repeat = {self.stream_count_repeat.__repr__()}'
		s += f'\n	* pad = {self.pad.__repr__()}'
		s += f'\n	* pad_dla = {self.pad_dla.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
