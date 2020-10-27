class LodInfo:

	"""
	Part of a mdl2 fragment, read for lodcount from one of the mdl2's fixed fragment entries
	20 bytes
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# usually first lod is 900
		self.distance = 0

		# unknown, found 0
		self.unknown_04 = 0

		# index of strzname from str pool later
		self.strznameidx = 0

		# first model for this lod in models list
		self.first_model_index = 0

		# not included in interval (python style indexing)
		self.last_model_index = 0

		# vertex count of lod
		self.vertex_count = 0

		# number of index entries in the triangle index list; (not: number of triangles, byte count of tri buffer)
		self.tri_index_count = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.distance = stream.read_float()
		self.unknown_04 = stream.read_ushort()
		self.strznameidx = stream.read_ushort()
		self.first_model_index = stream.read_ushort()
		self.last_model_index = stream.read_ushort()
		self.vertex_count = stream.read_uint()
		self.tri_index_count = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_float(self.distance)
		stream.write_ushort(self.unknown_04)
		stream.write_ushort(self.strznameidx)
		stream.write_ushort(self.first_model_index)
		stream.write_ushort(self.last_model_index)
		stream.write_uint(self.vertex_count)
		stream.write_uint(self.tri_index_count)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'LodInfo [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* distance = ' + self.distance.__repr__()
		s += '\n	* unknown_04 = ' + self.unknown_04.__repr__()
		s += '\n	* strznameidx = ' + self.strznameidx.__repr__()
		s += '\n	* first_model_index = ' + self.first_model_index.__repr__()
		s += '\n	* last_model_index = ' + self.last_model_index.__repr__()
		s += '\n	* vertex_count = ' + self.vertex_count.__repr__()
		s += '\n	* tri_index_count = ' + self.tri_index_count.__repr__()
		s += '\n'
		return s
