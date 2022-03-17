import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.MeshCollisionBit import MeshCollisionBit
from generated.formats.ms2.compound.Vector3 import Vector3


class MeshCollision:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.rotation = Matrix33(self.context, 0, None)

		# offset of mesh
		self.offset = Vector3(self.context, 0, None)

		# not floats, maybe 6 ushorts, shared among (all?) redwoods
		self.unk_1 = numpy.zeros((3, 2,), dtype=numpy.dtype('uint16'))

		# vertices (3 float)
		self.vertex_count = 0

		# tris?, counts the 25s at the end
		self.tri_count = 0

		# the smallest coordinates across all axes
		self.bounds_min = Vector3(self.context, 0, None)

		# the biggest coordinates across all axes
		self.bounds_max = Vector3(self.context, 0, None)

		# seemingly fixed
		self.ones_or_zeros = numpy.zeros((7,), dtype=numpy.dtype('uint64'))

		# seemingly fixed
		self.ff_or_zero = numpy.zeros((10,), dtype=numpy.dtype('int32'))

		# seemingly fixed
		self.ff_or_zero = numpy.zeros((8,), dtype=numpy.dtype('int32'))

		# verbatim
		self.bounds_min_repeat = Vector3(self.context, 0, None)

		# verbatim
		self.bounds_max_repeat = Vector3(self.context, 0, None)

		# seems to repeat tri_count
		self.tri_flags_count = 0

		# counts MeshCollisionBit
		self.count_bits = 0

		# ?
		self.stuff = numpy.zeros((9,), dtype=numpy.dtype('uint16'))

		# ?
		self.collision_bits = Array((self.count_bits,), MeshCollisionBit, self.context, 0, None)

		# always 25
		self.zeros = numpy.zeros((4,), dtype=numpy.dtype('uint32'))

		# array of vertices
		self.vertices = numpy.zeros((self.vertex_count, 3,), dtype=numpy.dtype('float32'))

		# triangle indices into vertex list
		self.triangles = numpy.zeros((self.tri_count, 3,), dtype=numpy.dtype('uint16'))

		# ?
		self.const = 0

		# always 25
		self.triangle_flags = numpy.zeros((self.tri_flags_count,), dtype=numpy.dtype('uint32'))

		# might be padding!
		self.zero_end = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.rotation = Matrix33(self.context, 0, None)
		self.offset = Vector3(self.context, 0, None)
		self.unk_1 = numpy.zeros((3, 2,), dtype=numpy.dtype('uint16'))
		self.vertex_count = 0
		self.tri_count = 0
		self.bounds_min = Vector3(self.context, 0, None)
		self.bounds_max = Vector3(self.context, 0, None)
		self.ones_or_zeros = numpy.zeros((7,), dtype=numpy.dtype('uint64'))
		if self.context.version <= 32:
			self.ff_or_zero = numpy.zeros((10,), dtype=numpy.dtype('int32'))
		if self.context.version >= 47:
			self.ff_or_zero = numpy.zeros((8,), dtype=numpy.dtype('int32'))
		if self.context.version <= 32:
			self.bounds_min_repeat = Vector3(self.context, 0, None)
		if self.context.version <= 32:
			self.bounds_max_repeat = Vector3(self.context, 0, None)
		if self.context.version <= 32:
			self.tri_flags_count = 0
		if self.context.version <= 32:
			self.count_bits = 0
		if self.context.version <= 32:
			self.stuff = numpy.zeros((9,), dtype=numpy.dtype('uint16'))
		if self.context.version <= 32:
			self.collision_bits = Array((self.count_bits,), MeshCollisionBit, self.context, 0, None)
		if self.context.version <= 32:
			self.zeros = numpy.zeros((4,), dtype=numpy.dtype('uint32'))
		self.vertices = numpy.zeros((self.vertex_count, 3,), dtype=numpy.dtype('float32'))
		self.triangles = numpy.zeros((self.tri_count, 3,), dtype=numpy.dtype('uint16'))
		if self.context.version <= 32:
			self.const = 0
		if self.context.version <= 32 and self.const:
			self.triangle_flags = numpy.zeros((self.tri_flags_count,), dtype=numpy.dtype('uint32'))
		self.zero_end = 0

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
		instance.rotation = Matrix33.from_stream(stream, instance.context, 0, None)
		instance.offset = Vector3.from_stream(stream, instance.context, 0, None)
		instance.unk_1 = stream.read_ushorts((3, 2,))
		instance.vertex_count = stream.read_uint64()
		instance.tri_count = stream.read_uint64()
		instance.bounds_min = Vector3.from_stream(stream, instance.context, 0, None)
		instance.bounds_max = Vector3.from_stream(stream, instance.context, 0, None)
		instance.ones_or_zeros = stream.read_uint64s((7,))
		if instance.context.version <= 32:
			instance.ff_or_zero = stream.read_ints((10,))
		if instance.context.version >= 47:
			instance.ff_or_zero = stream.read_ints((8,))
		if instance.context.version <= 32:
			instance.bounds_min_repeat = Vector3.from_stream(stream, instance.context, 0, None)
			instance.bounds_max_repeat = Vector3.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 32:
			instance.tri_flags_count = stream.read_uint()
			instance.count_bits = stream.read_ushort()
		if instance.context.version <= 32:
			instance.stuff = stream.read_ushorts((9,))
			instance.collision_bits = Array.from_stream(stream, (instance.count_bits,), MeshCollisionBit, instance.context, 0, None)
		if instance.context.version <= 32:
			instance.zeros = stream.read_uints((4,))
		instance.vertices = stream.read_floats((instance.vertex_count, 3,))
		instance.triangles = stream.read_ushorts((instance.tri_count, 3,))
		if instance.context.version <= 32:
			instance.const = stream.read_uint()
		if instance.context.version <= 32 and instance.const:
			instance.triangle_flags = stream.read_uints((instance.tri_flags_count,))
		instance.zero_end = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		Matrix33.to_stream(stream, instance.rotation)
		Vector3.to_stream(stream, instance.offset)
		stream.write_ushorts(instance.unk_1)
		stream.write_uint64(instance.vertex_count)
		stream.write_uint64(instance.tri_count)
		Vector3.to_stream(stream, instance.bounds_min)
		Vector3.to_stream(stream, instance.bounds_max)
		stream.write_uint64s(instance.ones_or_zeros)
		if instance.context.version <= 32:
			stream.write_ints(instance.ff_or_zero)
		if instance.context.version >= 47:
			stream.write_ints(instance.ff_or_zero)
		if instance.context.version <= 32:
			Vector3.to_stream(stream, instance.bounds_min_repeat)
			Vector3.to_stream(stream, instance.bounds_max_repeat)
		if instance.context.version <= 32:
			stream.write_uint(instance.tri_flags_count)
			stream.write_ushort(instance.count_bits)
		if instance.context.version <= 32:
			stream.write_ushorts(instance.stuff)
			Array.to_stream(stream, instance.collision_bits, (instance.count_bits,), MeshCollisionBit, instance.context, 0, None)
		if instance.context.version <= 32:
			stream.write_uints(instance.zeros)
		stream.write_floats(instance.vertices)
		stream.write_ushorts(instance.triangles)
		if instance.context.version <= 32:
			stream.write_uint(instance.const)
		if instance.context.version <= 32 and instance.const:
			stream.write_uints(instance.triangle_flags)
		stream.write_uint(instance.zero_end)

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
		return f'MeshCollision [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* rotation = {self.rotation.__repr__()}'
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* unk_1 = {self.unk_1.__repr__()}'
		s += f'\n	* vertex_count = {self.vertex_count.__repr__()}'
		s += f'\n	* tri_count = {self.tri_count.__repr__()}'
		s += f'\n	* bounds_min = {self.bounds_min.__repr__()}'
		s += f'\n	* bounds_max = {self.bounds_max.__repr__()}'
		s += f'\n	* ones_or_zeros = {self.ones_or_zeros.__repr__()}'
		s += f'\n	* ff_or_zero = {self.ff_or_zero.__repr__()}'
		s += f'\n	* bounds_min_repeat = {self.bounds_min_repeat.__repr__()}'
		s += f'\n	* bounds_max_repeat = {self.bounds_max_repeat.__repr__()}'
		s += f'\n	* tri_flags_count = {self.tri_flags_count.__repr__()}'
		s += f'\n	* count_bits = {self.count_bits.__repr__()}'
		s += f'\n	* stuff = {self.stuff.__repr__()}'
		s += f'\n	* collision_bits = {self.collision_bits.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* vertices = {self.vertices.__repr__()}'
		s += f'\n	* triangles = {self.triangles.__repr__()}'
		s += f'\n	* const = {self.const.__repr__()}'
		s += f'\n	* triangle_flags = {self.triangle_flags.__repr__()}'
		s += f'\n	* zero_end = {self.zero_end.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
