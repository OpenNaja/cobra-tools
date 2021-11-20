from generated.context import ContextReference


class LodInfo:

	"""
	Part of a mdl2 fragment, read for lodcount from one of the mdl2's fixed fragment entries
	20 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# usually first lod is 900
		self.distance = 0.0

		# always 0
		self.zero = 0

		# Last bone that is used by this lod's models; usually decreases with increasing lod index to decimate bones. However: JWE detailobjects - nat_groundcover_searocket_patchy_02 due to dedicated lod nodes
		self.bone_index = 0

		# first object for this lod in objects list
		self.first_object_index = 0

		# not included in interval (python style indexing)
		self.last_object_index = 0

		# vertex count of lod, sum of all vertex counts that are attached to this lod; rendered count, including duped models
		self.vertex_count = 0

		# number of index entries in the triangle index list; (not: number of triangles, byte count of tri buffer); rendered count, including duped models
		self.tri_index_count = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.distance = 0.0
		self.zero = 0
		self.bone_index = 0
		self.first_object_index = 0
		self.last_object_index = 0
		self.vertex_count = 0
		self.tri_index_count = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.distance = stream.read_float()
		self.zero = stream.read_ushort()
		self.bone_index = stream.read_ushort()
		self.first_object_index = stream.read_ushort()
		self.last_object_index = stream.read_ushort()
		self.vertex_count = stream.read_uint()
		self.tri_index_count = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_float(self.distance)
		stream.write_ushort(self.zero)
		stream.write_ushort(self.bone_index)
		stream.write_ushort(self.first_object_index)
		stream.write_ushort(self.last_object_index)
		stream.write_uint(self.vertex_count)
		stream.write_uint(self.tri_index_count)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'LodInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* distance = {self.distance.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* bone_index = {self.bone_index.__repr__()}'
		s += f'\n	* first_object_index = {self.first_object_index.__repr__()}'
		s += f'\n	* last_object_index = {self.last_object_index.__repr__()}'
		s += f'\n	* vertex_count = {self.vertex_count.__repr__()}'
		s += f'\n	* tri_index_count = {self.tri_index_count.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
