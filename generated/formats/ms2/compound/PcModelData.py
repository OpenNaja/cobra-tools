import typing


class PcModelData:

	"""
	Defines one model's data. Both LODs and mdl2 files may contain several of these.
	This is a fragment from headers of type (0,0)
	If there is more than one of these, the fragments appear as a list according to
	"""

	# always zero

	# always zero
	zeros: typing.List[int]

	# repeat
	tri_index_count_a: int

	# vertex count of model
	vertex_count: int

	# byte offset from start of tri buffer in bytes
	tri_offset: int

	# number of index entries in the triangle index list; (not: number of triangles, byte count of tri buffer)
	tri_index_count: int

	# byte offset from start of vert buffer (=start of buffer nr 2) in bytes
	vertex_offset: int

	# always zero
	unknown_05: int

	# ?
	weight_offset: int

	# ?
	vert_offset_within_lod: int

	# power of 2 increasing with lod index
	poweroftwo: int

	# always zero
	zero: int

	# some floats
	unknown_07: float

	# maybe a bitfield; usually in 500 range, e.g 513 (parrot, JWE trees), 517 (stairwell, PZ trees), 529 (driver, PZ terrarium animals)
	flag: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.zeros = []
		self.tri_index_count_a = 0
		self.vertex_count = 0
		self.tri_offset = 0
		self.tri_index_count = 0
		self.vertex_offset = 0
		self.unknown_05 = 0
		self.weight_offset = 0
		self.zeros = []
		self.vert_offset_within_lod = 0
		self.poweroftwo = 0
		self.zero = 0
		self.unknown_07 = 0
		self.flag = 0

	def read(self, stream):

		io_start = stream.tell()
		self.zeros = [stream.read_uint() for _ in range(4)]
		if stream.ms_2_version == 32:
			self.tri_index_count_a = stream.read_uint()
		self.vertex_count = stream.read_uint()
		self.tri_offset = stream.read_uint()
		self.tri_index_count = stream.read_uint()
		self.vertex_offset = stream.read_uint()
		self.unknown_05 = stream.read_uint()
		self.weight_offset = stream.read_uint()
		self.zeros = [stream.read_uint() for _ in range(2)]
		self.vert_offset_within_lod = stream.read_uint()
		self.poweroftwo = stream.read_uint()
		self.zero = stream.read_uint()
		self.unknown_07 = stream.read_float()
		self.flag = stream.read_uint()

		self.io_size = stream.tell() - io_start

	def write(self, stream):

		io_start = stream.tell()
		for item in self.zeros: stream.write_uint(item)
		if stream.ms_2_version == 32:
			stream.write_uint(self.tri_index_count_a)
		stream.write_uint(self.vertex_count)
		stream.write_uint(self.tri_offset)
		stream.write_uint(self.tri_index_count)
		stream.write_uint(self.vertex_offset)
		stream.write_uint(self.unknown_05)
		stream.write_uint(self.weight_offset)
		for item in self.zeros: stream.write_uint(item)
		stream.write_uint(self.vert_offset_within_lod)
		stream.write_uint(self.poweroftwo)
		stream.write_uint(self.zero)
		stream.write_float(self.unknown_07)
		stream.write_uint(self.flag)

		self.io_size = stream.tell() - io_start

	def __repr__(self):
		s = 'PcModelData [Size: '+str(self.io_size)+']'
		s += '\n	* zeros = ' + self.zeros.__repr__()
		s += '\n	* tri_index_count_a = ' + self.tri_index_count_a.__repr__()
		s += '\n	* vertex_count = ' + self.vertex_count.__repr__()
		s += '\n	* tri_offset = ' + self.tri_offset.__repr__()
		s += '\n	* tri_index_count = ' + self.tri_index_count.__repr__()
		s += '\n	* vertex_offset = ' + self.vertex_offset.__repr__()
		s += '\n	* unknown_05 = ' + self.unknown_05.__repr__()
		s += '\n	* weight_offset = ' + self.weight_offset.__repr__()
		s += '\n	* vert_offset_within_lod = ' + self.vert_offset_within_lod.__repr__()
		s += '\n	* poweroftwo = ' + self.poweroftwo.__repr__()
		s += '\n	* zero = ' + self.zero.__repr__()
		s += '\n	* unknown_07 = ' + self.unknown_07.__repr__()
		s += '\n	* flag = ' + self.flag.__repr__()
		s += '\n'
		return s
