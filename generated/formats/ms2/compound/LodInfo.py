from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class LodInfo:

	"""
	Part of a mdl2 fragment, read for lodcount from one of the mdl2's fixed fragment entries
	20 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
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
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.distance = stream.read_float()
		instance.zero = stream.read_ushort()
		instance.bone_index = stream.read_ushort()
		instance.first_object_index = stream.read_ushort()
		instance.last_object_index = stream.read_ushort()
		instance.vertex_count = stream.read_uint()
		instance.tri_index_count = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_float(instance.distance)
		stream.write_ushort(instance.zero)
		stream.write_ushort(instance.bone_index)
		stream.write_ushort(instance.first_object_index)
		stream.write_ushort(instance.last_object_index)
		stream.write_uint(instance.vertex_count)
		stream.write_uint(instance.tri_index_count)

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

	def get_info_str(self, indent=0):
		return f'LodInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* distance = {fmt_member(self.distance, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		s += f'\n	* bone_index = {fmt_member(self.bone_index, indent+1)}'
		s += f'\n	* first_object_index = {fmt_member(self.first_object_index, indent+1)}'
		s += f'\n	* last_object_index = {fmt_member(self.last_object_index, indent+1)}'
		s += f'\n	* vertex_count = {fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* tri_index_count = {fmt_member(self.tri_index_count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
