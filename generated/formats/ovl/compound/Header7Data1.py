import typing
from generated.array import Array
from generated.formats.ovl.compound.Header7MipmapInfo import Header7MipmapInfo


class Header7Data1:

	"""
	Data struct for headers of type 7
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zero_00 = 0
		self.zero_04 = 0

		# total dds buffer size
		self.data_size = 0
		self.width = 0
		self.height = 0

		# aka tile_width; may be depth
		self.depth = 0

		# aka tile_height; may be array_size
		self.array_size = 0

		# num_mips ??
		self.num_mips = 0

		# skipped by barbasol
		self.pad = 0
		self.mip_maps = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.zero_00 = stream.read_uint()
		self.zero_04 = stream.read_uint()
		self.data_size = stream.read_uint()
		self.width = stream.read_uint()
		self.height = stream.read_uint()
		self.depth = stream.read_uint()
		self.array_size = stream.read_uint()
		self.num_mips = stream.read_uint()
		self.pad = stream.read_byte()
		self.mip_maps.read(stream, Header7MipmapInfo, self.num_mips, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.zero_00)
		stream.write_uint(self.zero_04)
		stream.write_uint(self.data_size)
		stream.write_uint(self.width)
		stream.write_uint(self.height)
		stream.write_uint(self.depth)
		stream.write_uint(self.array_size)
		stream.write_uint(self.num_mips)
		stream.write_byte(self.pad)
		self.mip_maps.write(stream, Header7MipmapInfo, self.num_mips, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Header7Data1 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zero_00 = {self.zero_00.__repr__()}'
		s += f'\n	* zero_04 = {self.zero_04.__repr__()}'
		s += f'\n	* data_size = {self.data_size.__repr__()}'
		s += f'\n	* width = {self.width.__repr__()}'
		s += f'\n	* height = {self.height.__repr__()}'
		s += f'\n	* depth = {self.depth.__repr__()}'
		s += f'\n	* array_size = {self.array_size.__repr__()}'
		s += f'\n	* num_mips = {self.num_mips.__repr__()}'
		s += f'\n	* pad = {self.pad.__repr__()}'
		s += f'\n	* mip_maps = {self.mip_maps.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
