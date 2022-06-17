from source.formats.base.basic import fmt_member
import numpy
from generated.formats.ms2.compound.MeshData import MeshData


class BioMeshData(MeshData):

	"""
	PZ, JWE2 - 64 bytes incl. inheritance
	JWE2 - 48 bytes incl. inheritance
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# unk
		self.a_offset = 0

		# unk
		self.a_size = 0

		# vertex count of model
		self.vertex_count = 0

		# number of index entries in the triangle index list; (not: number of triangles, byte count of tri buffer)
		self.tri_index_count = 0

		# unk, may be used in other models
		self.zero_1 = 0

		# power of 2 increasing with lod index
		self.poweroftwo = 0

		# some floats, purpose unknown
		self.unk_floats = numpy.zeros((2,), dtype=numpy.dtype('float32'))

		# always 1
		self.one = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if (self.context.version == 51) and self.context.biosyn:
			self.a_offset = 0
		if (self.context.version == 51) and self.context.biosyn:
			self.a_size = 0
		self.vertex_count = 0
		self.tri_index_count = 0
		self.zero_1 = 0
		self.poweroftwo = 0
		self.unk_floats = numpy.zeros((2,), dtype=numpy.dtype('float32'))
		self.one = 0

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
		super().read_fields(stream, instance)
		if (instance.context.version == 51) and instance.context.biosyn:
			instance.a_offset = stream.read_uint()
			instance.a_size = stream.read_uint()
		instance.vertex_count = stream.read_uint()
		instance.tri_index_count = stream.read_uint()
		instance.zero_1 = stream.read_uint64()
		instance.poweroftwo = stream.read_uint()
		instance.unk_floats = stream.read_floats((2,))
		instance.one = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if (instance.context.version == 51) and instance.context.biosyn:
			stream.write_uint(instance.a_offset)
			stream.write_uint(instance.a_size)
		stream.write_uint(instance.vertex_count)
		stream.write_uint(instance.tri_index_count)
		stream.write_uint64(instance.zero_1)
		stream.write_uint(instance.poweroftwo)
		stream.write_floats(instance.unk_floats)
		stream.write_uint(instance.one)

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
		return f'BioMeshData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* a_offset = {fmt_member(self.a_offset, indent+1)}'
		s += f'\n	* a_size = {fmt_member(self.a_size, indent+1)}'
		s += f'\n	* vertex_count = {fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* tri_index_count = {fmt_member(self.tri_index_count, indent+1)}'
		s += f'\n	* zero_1 = {fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* poweroftwo = {fmt_member(self.poweroftwo, indent+1)}'
		s += f'\n	* unk_floats = {fmt_member(self.unk_floats, indent+1)}'
		s += f'\n	* one = {fmt_member(self.one, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
