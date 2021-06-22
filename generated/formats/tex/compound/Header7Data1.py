import numpy
import typing
from generated.array import Array
from generated.formats.tex.compound.Header7MipmapInfo import Header7MipmapInfo


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

		# zero
		self.zero = 0

		# total dds buffer size
		self.data_size = 0

		# x size in pixels
		self.width = 0

		# y size in pixels
		self.height = 0

		# aka tile_width; may be depth
		self.depth = 0

		# aka tile_height; may be array_size
		self.array_size = 0

		# amount of mip map levels
		self.num_mips = 0

		# skipped by barbasol
		self.pad = 0

		# only found in PZ
		self.unk_pz = 0

		# info about mip levels
		self.mip_maps = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.zero = stream.read_uint64()
		self.data_size = stream.read_uint()
		self.width = stream.read_uint()
		self.height = stream.read_uint()
		self.depth = stream.read_uint()
		self.array_size = stream.read_uint()
		self.num_mips = stream.read_uint()
		self.pad = stream.read_byte()
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version >= 19):
			self.unk_pz = stream.read_uint64()
		self.mip_maps.read(stream, Header7MipmapInfo, self.num_mips, None)

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
		stream.write_byte(self.pad)
		if ((stream.user_version == 8340) or (stream.user_version == 8724)) and (stream.version >= 19):
			stream.write_uint64(self.unk_pz)
		self.mip_maps.write(stream, Header7MipmapInfo, self.num_mips, None)

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
		s += f'\n	* pad = {self.pad.__repr__()}'
		s += f'\n	* unk_pz = {self.unk_pz.__repr__()}'
		s += f'\n	* mip_maps = {self.mip_maps.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
