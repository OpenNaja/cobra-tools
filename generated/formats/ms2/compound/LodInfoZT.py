class LodInfoZT:

	"""
	Part of a mdl2 fragment, read for lodcount from one of the mdl2's fixed fragment entries
	20 bytes
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# FFFF
		self.full = 0

		# 7F7F
		self.half = 0

		# increasing
		self.lod_index = 0

		# index of the bone in this model's bone info that this lod level is attached to (good example: JWE detailobjects - nat_groundcover_searocket_patchy_02)
		self.bone_index = 0

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
		self.full = stream.read_short()
		self.half = stream.read_short()
		self.lod_index = stream.read_ushort()
		self.bone_index = stream.read_ushort()
		self.first_model_index = stream.read_ushort()
		self.last_model_index = stream.read_ushort()
		self.vertex_count = stream.read_ushort()
		self.tri_index_count = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_short(self.full)
		stream.write_short(self.half)
		stream.write_ushort(self.lod_index)
		stream.write_ushort(self.bone_index)
		stream.write_ushort(self.first_model_index)
		stream.write_ushort(self.last_model_index)
		stream.write_ushort(self.vertex_count)
		stream.write_ushort(self.tri_index_count)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'LodInfoZT [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* full = {self.full.__repr__()}'
		s += f'\n	* half = {self.half.__repr__()}'
		s += f'\n	* lod_index = {self.lod_index.__repr__()}'
		s += f'\n	* bone_index = {self.bone_index.__repr__()}'
		s += f'\n	* first_model_index = {self.first_model_index.__repr__()}'
		s += f'\n	* last_model_index = {self.last_model_index.__repr__()}'
		s += f'\n	* vertex_count = {self.vertex_count.__repr__()}'
		s += f'\n	* tri_index_count = {self.tri_index_count.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
