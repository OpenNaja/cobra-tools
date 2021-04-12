import typing
from generated.array import Array
from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.Vector3 import Vector3


class UnkHull:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.rotation = Matrix33()

		# ?
		self.unk_0 = Vector3()

		# not floats, maybe 6 ushorts, shared among (all?) redwoods
		self.unk_1 = Vector3()

		# vertices (3 float)
		self.vertex_count = 0

		# tris?, counts the 25s at the end
		self.tri_count = 0

		# ?
		self.unk_2 = Vector3()

		# ?
		self.unk_3 = Vector3()

		# seemingly fixed
		self.ones_or_zeros = Array()

		# seemingly fixed
		self.ff_or_zero = Array()

		# ?
		self.unk_4 = Vector3()

		# ?
		self.unk_5 = Vector3()

		# ?
		self.countc = 0

		# ?
		self.stuff = Array()

		# ?
		self.countd = 0

		# ?
		self.consts = Array()

		# ?
		self.zeros = Array()

		# array of vertices
		self.vertices = Array()

		# triangle indices into vertex list
		self.triangles = Array()

		# ?
		self.const = 0

		# always 25
		self.triangle_flags = Array()

		# ?
		self.zero_end = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.rotation = stream.read_type(Matrix33)
		self.unk_0 = stream.read_type(Vector3)
		self.unk_1 = stream.read_type(Vector3)
		self.vertex_count = stream.read_uint64()
		self.tri_count = stream.read_uint64()
		self.unk_2 = stream.read_type(Vector3)
		self.unk_3 = stream.read_type(Vector3)
		self.ones_or_zeros = stream.read_uint64s((7))
		self.ff_or_zero = stream.read_ints((10))
		self.unk_4 = stream.read_type(Vector3)
		self.unk_5 = stream.read_type(Vector3)
		self.countc = stream.read_uint()
		self.stuff = stream.read_ushorts((43))
		self.countd = stream.read_ushort()
		self.consts = stream.read_uints((3))
		self.zeros = stream.read_uints((4))
		self.vertices.read(stream, Vector3, self.vertex_count, None)
		self.triangles = stream.read_ushorts((self.tri_count, 3))
		self.const = stream.read_uint()
		self.triangle_flags = stream.read_uints((self.tri_count))
		self.zero_end = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.rotation)
		stream.write_type(self.unk_0)
		stream.write_type(self.unk_1)
		stream.write_uint64(self.vertex_count)
		stream.write_uint64(self.tri_count)
		stream.write_type(self.unk_2)
		stream.write_type(self.unk_3)
		stream.write_uint64s(self.ones_or_zeros)
		stream.write_ints(self.ff_or_zero)
		stream.write_type(self.unk_4)
		stream.write_type(self.unk_5)
		stream.write_uint(self.countc)
		stream.write_ushorts(self.stuff)
		stream.write_ushort(self.countd)
		stream.write_uints(self.consts)
		stream.write_uints(self.zeros)
		self.vertices.write(stream, Vector3, self.vertex_count, None)
		stream.write_ushorts(self.triangles)
		stream.write_uint(self.const)
		stream.write_uints(self.triangle_flags)
		stream.write_uint(self.zero_end)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'UnkHull [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* rotation = {self.rotation.__repr__()}'
		s += f'\n	* unk_0 = {self.unk_0.__repr__()}'
		s += f'\n	* unk_1 = {self.unk_1.__repr__()}'
		s += f'\n	* vertex_count = {self.vertex_count.__repr__()}'
		s += f'\n	* tri_count = {self.tri_count.__repr__()}'
		s += f'\n	* unk_2 = {self.unk_2.__repr__()}'
		s += f'\n	* unk_3 = {self.unk_3.__repr__()}'
		s += f'\n	* ones_or_zeros = {self.ones_or_zeros.__repr__()}'
		s += f'\n	* ff_or_zero = {self.ff_or_zero.__repr__()}'
		s += f'\n	* unk_4 = {self.unk_4.__repr__()}'
		s += f'\n	* unk_5 = {self.unk_5.__repr__()}'
		s += f'\n	* countc = {self.countc.__repr__()}'
		s += f'\n	* stuff = {self.stuff.__repr__()}'
		s += f'\n	* countd = {self.countd.__repr__()}'
		s += f'\n	* consts = {self.consts.__repr__()}'
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
