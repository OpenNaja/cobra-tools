import typing
from generated.formats.ovl.compound.Header7MipmapInfo import Header7MipmapInfo


class Header7Data1:

# Data struct for headers of type 7
	zero_00: int
	zero_04: int

	# total dds buffer size
	data_size: int
	width: int
	height: int

	# aka tile_width; may be depth
	depth: int

	# aka tile_height; may be array_size
	array_size: int

	# num_mips ??
	num_mips: int

	# skipped by barbasol
	pad: int
	mip_maps: typing.List[Header7MipmapInfo]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.zero_00 = stream.read_uint()
		self.zero_04 = stream.read_uint()
		self.data_size = stream.read_uint()
		self.width = stream.read_uint()
		self.height = stream.read_uint()
		self.depth = stream.read_uint()
		self.array_size = stream.read_uint()
		self.num_mips = stream.read_uint()
		self.pad = stream.read_byte()
		self.mip_maps = [stream.read_type(Header7MipmapInfo) for _ in range(self.num_mips)]

	def write(self, stream):
		stream.write_uint(self.zero_00)
		stream.write_uint(self.zero_04)
		stream.write_uint(self.data_size)
		stream.write_uint(self.width)
		stream.write_uint(self.height)
		stream.write_uint(self.depth)
		stream.write_uint(self.array_size)
		stream.write_uint(self.num_mips)
		stream.write_byte(self.pad)
		for item in self.mip_maps: stream.write_type(item)

	def __repr__(self):
		s = 'Header7Data1'
		s += '\nzero_00 ' + self.zero_00.__repr__()
		s += '\nzero_04 ' + self.zero_04.__repr__()
		s += '\ndata_size ' + self.data_size.__repr__()
		s += '\nwidth ' + self.width.__repr__()
		s += '\nheight ' + self.height.__repr__()
		s += '\ndepth ' + self.depth.__repr__()
		s += '\narray_size ' + self.array_size.__repr__()
		s += '\nnum_mips ' + self.num_mips.__repr__()
		s += '\npad ' + self.pad.__repr__()
		s += '\nmip_maps ' + self.mip_maps.__repr__()
		s += '\n'
		return s