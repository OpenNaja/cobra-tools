import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.MeshCollisionBit import MeshCollisionBit
from generated.formats.ms2.compound.Vector3 import Vector3


class MeshCollision:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.rotation = Matrix33(self.context, None, None)

		# offset of mesh
		self.offset = Vector3(self.context, None, None)

		# not floats, maybe 6 ushorts, shared among (all?) redwoods
		self.unk_1 = numpy.zeros((3, 2), dtype=numpy.dtype('uint16'))

		# vertices (3 float)
		self.vertex_count = 0

		# tris?, counts the 25s at the end
		self.tri_count = 0

		# the smallest coordinates across all axes
		self.bounds_min = Vector3(self.context, None, None)

		# the biggest coordinates across all axes
		self.bounds_max = Vector3(self.context, None, None)

		# seemingly fixed
		self.ones_or_zeros = numpy.zeros((7), dtype=numpy.dtype('uint64'))

		# seemingly fixed
		self.ff_or_zero = numpy.zeros((10), dtype=numpy.dtype('int32'))

		# verbatim
		self.bounds_min_repeat = Vector3(self.context, None, None)

		# verbatim
		self.bounds_max_repeat = Vector3(self.context, None, None)

		# seems to repeat tri_count
		self.tri_flags_count = 0

		# counts MeshCollisionBit
		self.count_bits = 0

		# ?
		self.stuff = numpy.zeros((9), dtype=numpy.dtype('uint16'))

		# ?
		self.collision_bits = Array((self.count_bits), MeshCollisionBit, self.context, None, None)

		# always 25
		self.zeros = numpy.zeros((4), dtype=numpy.dtype('uint32'))

		# array of vertices
		self.vertices = numpy.zeros((self.vertex_count, 3), dtype=numpy.dtype('float32'))

		# triangle indices into vertex list
		self.triangles = numpy.zeros((self.tri_count, 3), dtype=numpy.dtype('uint16'))

		# ?
		self.const = 0

		# always 25
		self.triangle_flags = numpy.zeros((self.tri_flags_count), dtype=numpy.dtype('uint32'))

		# might be padding!
		self.zero_end = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.rotation = Matrix33(self.context, None, None)
		self.offset = Vector3(self.context, None, None)
		self.unk_1 = numpy.zeros((3, 2), dtype=numpy.dtype('uint16'))
		self.vertex_count = 0
		self.tri_count = 0
		self.bounds_min = Vector3(self.context, None, None)
		self.bounds_max = Vector3(self.context, None, None)
		self.ones_or_zeros = numpy.zeros((7), dtype=numpy.dtype('uint64'))
		self.ff_or_zero = numpy.zeros((10), dtype=numpy.dtype('int32'))
		self.bounds_min_repeat = Vector3(self.context, None, None)
		self.bounds_max_repeat = Vector3(self.context, None, None)
		self.tri_flags_count = 0
		self.count_bits = 0
		self.stuff = numpy.zeros((9), dtype=numpy.dtype('uint16'))
		self.collision_bits = Array((self.count_bits), MeshCollisionBit, self.context, None, None)
		self.zeros = numpy.zeros((4), dtype=numpy.dtype('uint32'))
		self.vertices = numpy.zeros((self.vertex_count, 3), dtype=numpy.dtype('float32'))
		self.triangles = numpy.zeros((self.tri_count, 3), dtype=numpy.dtype('uint16'))
		self.const = 0
		if self.const:
			self.triangle_flags = numpy.zeros((self.tri_flags_count), dtype=numpy.dtype('uint32'))
		self.zero_end = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.rotation = stream.read_type(Matrix33, (self.context, None, None))
		self.offset = stream.read_type(Vector3, (self.context, None, None))
		self.unk_1 = stream.read_ushorts((3, 2))
		self.vertex_count = stream.read_uint64()
		self.tri_count = stream.read_uint64()
		self.bounds_min = stream.read_type(Vector3, (self.context, None, None))
		self.bounds_max = stream.read_type(Vector3, (self.context, None, None))
		self.ones_or_zeros = stream.read_uint64s((7))
		self.ff_or_zero = stream.read_ints((10))
		self.bounds_min_repeat = stream.read_type(Vector3, (self.context, None, None))
		self.bounds_max_repeat = stream.read_type(Vector3, (self.context, None, None))
		self.tri_flags_count = stream.read_uint()
		self.count_bits = stream.read_ushort()
		self.stuff = stream.read_ushorts((9))
		self.collision_bits.read(stream, MeshCollisionBit, self.count_bits, None)
		self.zeros = stream.read_uints((4))
		self.vertices = stream.read_floats((self.vertex_count, 3))
		self.triangles = stream.read_ushorts((self.tri_count, 3))
		self.const = stream.read_uint()
		if self.const:
			self.triangle_flags = stream.read_uints((self.tri_flags_count))
		self.zero_end = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.rotation)
		stream.write_type(self.offset)
		stream.write_ushorts(self.unk_1)
		stream.write_uint64(self.vertex_count)
		stream.write_uint64(self.tri_count)
		stream.write_type(self.bounds_min)
		stream.write_type(self.bounds_max)
		stream.write_uint64s(self.ones_or_zeros)
		stream.write_ints(self.ff_or_zero)
		stream.write_type(self.bounds_min_repeat)
		stream.write_type(self.bounds_max_repeat)
		stream.write_uint(self.tri_flags_count)
		stream.write_ushort(self.count_bits)
		stream.write_ushorts(self.stuff)
		self.collision_bits.write(stream, MeshCollisionBit, self.count_bits, None)
		stream.write_uints(self.zeros)
		stream.write_floats(self.vertices)
		stream.write_ushorts(self.triangles)
		stream.write_uint(self.const)
		if self.const:
			stream.write_uints(self.triangle_flags)
		stream.write_uint(self.zero_end)

		self.io_size = stream.tell() - self.io_start

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
