from generated.array import Array
from generated.context import ContextReference
from generated.formats.tex.compound.Mipmap import Mipmap


class Header7Data1:

	"""
	Data struct for headers of type 7
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# zero
		self.zero = 0

		# total dds buffer size
		self.data_size = 0

		# x size in pixels
		self.width = 0

		# y size in pixels
		self.height = 0

		# may be depth
		self.depth = 0

		# amount of repeats of the data for each lod
		self.array_size = 0

		# amount of mip map levels
		self.num_mips = 0

		# only found in PZ and JWE2
		self.unk_pz = 0

		# info about mip levels
		self.mip_maps = Array((self.num_mips), Mipmap, self.context, None, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.zero = 0
		self.data_size = 0
		self.width = 0
		self.height = 0
		self.depth = 0
		self.array_size = 0
		self.num_mips = 0
		if self.context.version >= 20:
			self.unk_pz = 0
		self.mip_maps = Array((self.num_mips), Mipmap, self.context, None, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.zero = stream.read_uint64()
		self.data_size = stream.read_uint()
		self.width = stream.read_uint()
		self.height = stream.read_uint()
		self.depth = stream.read_uint()
		self.array_size = stream.read_uint()
		self.num_mips = stream.read_uint()
		if self.context.version >= 20:
			self.unk_pz = stream.read_uint64()
		self.mip_maps.read(stream, Mipmap, self.num_mips, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.zero)
		stream.write_uint(self.data_size)
		stream.write_uint(self.width)
		stream.write_uint(self.height)
		stream.write_uint(self.depth)
		stream.write_uint(self.array_size)
		stream.write_uint(self.num_mips)
		if self.context.version >= 20:
			stream.write_uint64(self.unk_pz)
		self.mip_maps.write(stream, Mipmap, self.num_mips, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Header7Data1 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* data_size = {self.data_size.__repr__()}'
		s += f'\n	* width = {self.width.__repr__()}'
		s += f'\n	* height = {self.height.__repr__()}'
		s += f'\n	* depth = {self.depth.__repr__()}'
		s += f'\n	* array_size = {self.array_size.__repr__()}'
		s += f'\n	* num_mips = {self.num_mips.__repr__()}'
		s += f'\n	* unk_pz = {self.unk_pz.__repr__()}'
		s += f'\n	* mip_maps = {self.mip_maps.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
