import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.MeshCollisionBit import MeshCollisionBit
from generated.formats.ms2.compound.Vector3 import Vector3


class MeshCollision(BaseStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.rotation = 0

		# offset of mesh
		self.offset = 0

		# not floats, maybe 6 ushorts, shared among (all?) redwoods
		self.unk_1 = 0

		# vertices (3 float)
		self.vertex_count = 0

		# tris?, counts the 25s at the end
		self.tri_count = 0

		# the smallest coordinates across all axes
		self.bounds_min = 0

		# the biggest coordinates across all axes
		self.bounds_max = 0

		# seemingly fixed
		self.ones_or_zeros = 0

		# seemingly fixed
		self.ff_or_zero = 0

		# verbatim
		self.bounds_min_repeat = 0

		# verbatim
		self.bounds_max_repeat = 0

		# seems to repeat tri_count
		self.tri_flags_count = 0

		# counts MeshCollisionBit
		self.count_bits = 0

		# ?
		self.stuff = 0

		# ?
		self.collision_bits = 0

		# always 25
		self.zeros = 0

		# array of vertices
		self.vertices = 0

		# triangle indices into vertex list
		self.triangles = 0

		# ?
		self.const = 0

		# always 25
		self.triangle_flags = 0

		# might be padding!
		self.zero_end = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
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
			self.bounds_max_repeat = Vector3(self.context, 0, None)
			self.tri_flags_count = 0
			self.count_bits = 0
			self.stuff = numpy.zeros((9,), dtype=numpy.dtype('uint16'))
			self.collision_bits = Array((self.count_bits,), MeshCollisionBit, self.context, 0, None)
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
		super().read_fields(stream, instance)
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
			instance.tri_flags_count = stream.read_uint()
			instance.count_bits = stream.read_ushort()
			instance.stuff = stream.read_ushorts((9,))
			instance.collision_bits = Array.from_stream(stream, (instance.count_bits,), MeshCollisionBit, instance.context, 0, None)
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
		super().write_fields(stream, instance)
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
			stream.write_uint(instance.tri_flags_count)
			stream.write_ushort(instance.count_bits)
			stream.write_ushorts(instance.stuff)
			Array.to_stream(stream, instance.collision_bits, (instance.count_bits,), MeshCollisionBit, instance.context, 0, None)
			stream.write_uints(instance.zeros)
		stream.write_floats(instance.vertices)
		stream.write_ushorts(instance.triangles)
		if instance.context.version <= 32:
			stream.write_uint(instance.const)
		if instance.context.version <= 32 and instance.const:
			stream.write_uints(instance.triangle_flags)
		stream.write_uint(instance.zero_end)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('rotation', Matrix33, (0, None))
		yield ('offset', Vector3, (0, None))
		yield ('unk_1', Array, ((3, 2,), Ushort, 0, None))
		yield ('vertex_count', Uint64, (0, None))
		yield ('tri_count', Uint64, (0, None))
		yield ('bounds_min', Vector3, (0, None))
		yield ('bounds_max', Vector3, (0, None))
		yield ('ones_or_zeros', Array, ((7,), Uint64, 0, None))
		if instance.context.version <= 32:
			yield ('ff_or_zero', Array, ((10,), Int, 0, None))
		if instance.context.version >= 47:
			yield ('ff_or_zero', Array, ((8,), Int, 0, None))
		if instance.context.version <= 32:
			yield ('bounds_min_repeat', Vector3, (0, None))
			yield ('bounds_max_repeat', Vector3, (0, None))
			yield ('tri_flags_count', Uint, (0, None))
			yield ('count_bits', Ushort, (0, None))
			yield ('stuff', Array, ((9,), Ushort, 0, None))
			yield ('collision_bits', Array, ((instance.count_bits,), MeshCollisionBit, 0, None))
			yield ('zeros', Array, ((4,), Uint, 0, None))
		yield ('vertices', Array, ((instance.vertex_count, 3,), Float, 0, None))
		yield ('triangles', Array, ((instance.tri_count, 3,), Ushort, 0, None))
		if instance.context.version <= 32:
			yield ('const', Uint, (0, None))
		if instance.context.version <= 32 and instance.const:
			yield ('triangle_flags', Array, ((instance.tri_flags_count,), Uint, 0, None))
		yield ('zero_end', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'MeshCollision [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* rotation = {self.fmt_member(self.rotation, indent+1)}'
		s += f'\n	* offset = {self.fmt_member(self.offset, indent+1)}'
		s += f'\n	* unk_1 = {self.fmt_member(self.unk_1, indent+1)}'
		s += f'\n	* vertex_count = {self.fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* tri_count = {self.fmt_member(self.tri_count, indent+1)}'
		s += f'\n	* bounds_min = {self.fmt_member(self.bounds_min, indent+1)}'
		s += f'\n	* bounds_max = {self.fmt_member(self.bounds_max, indent+1)}'
		s += f'\n	* ones_or_zeros = {self.fmt_member(self.ones_or_zeros, indent+1)}'
		s += f'\n	* ff_or_zero = {self.fmt_member(self.ff_or_zero, indent+1)}'
		s += f'\n	* bounds_min_repeat = {self.fmt_member(self.bounds_min_repeat, indent+1)}'
		s += f'\n	* bounds_max_repeat = {self.fmt_member(self.bounds_max_repeat, indent+1)}'
		s += f'\n	* tri_flags_count = {self.fmt_member(self.tri_flags_count, indent+1)}'
		s += f'\n	* count_bits = {self.fmt_member(self.count_bits, indent+1)}'
		s += f'\n	* stuff = {self.fmt_member(self.stuff, indent+1)}'
		s += f'\n	* collision_bits = {self.fmt_member(self.collision_bits, indent+1)}'
		s += f'\n	* zeros = {self.fmt_member(self.zeros, indent+1)}'
		s += f'\n	* vertices = {self.fmt_member(self.vertices, indent+1)}'
		s += f'\n	* triangles = {self.fmt_member(self.triangles, indent+1)}'
		s += f'\n	* const = {self.fmt_member(self.const, indent+1)}'
		s += f'\n	* triangle_flags = {self.fmt_member(self.triangle_flags, indent+1)}'
		s += f'\n	* zero_end = {self.fmt_member(self.zero_end, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
