from generated.context import ContextReference


class LodInfoZT:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
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
		self.first_object_index = 0

		# not included in interval (python style indexing)
		self.some_index = 0

		# vertex count of lod
		self.some_index_2 = 0

		# number of index entries in the triangle index list; (not: number of triangles, byte count of tri buffer)
		self.last_object_index = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.full = 0
		self.half = 0
		self.lod_index = 0
		self.bone_index = 0
		self.first_object_index = 0
		self.some_index = 0
		self.some_index_2 = 0
		self.last_object_index = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.full = stream.read_short()
		instance.half = stream.read_short()
		instance.lod_index = stream.read_ushort()
		instance.bone_index = stream.read_ushort()
		instance.first_object_index = stream.read_ushort()
		instance.some_index = stream.read_ushort()
		instance.some_index_2 = stream.read_ushort()
		instance.last_object_index = stream.read_ushort()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_short(instance.full)
		stream.write_short(instance.half)
		stream.write_ushort(instance.lod_index)
		stream.write_ushort(instance.bone_index)
		stream.write_ushort(instance.first_object_index)
		stream.write_ushort(instance.some_index)
		stream.write_ushort(instance.some_index_2)
		stream.write_ushort(instance.last_object_index)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self):
		return f'LodInfoZT [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* full = {self.full.__repr__()}'
		s += f'\n	* half = {self.half.__repr__()}'
		s += f'\n	* lod_index = {self.lod_index.__repr__()}'
		s += f'\n	* bone_index = {self.bone_index.__repr__()}'
		s += f'\n	* first_object_index = {self.first_object_index.__repr__()}'
		s += f'\n	* some_index = {self.some_index.__repr__()}'
		s += f'\n	* some_index_2 = {self.some_index_2.__repr__()}'
		s += f'\n	* last_object_index = {self.last_object_index.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
