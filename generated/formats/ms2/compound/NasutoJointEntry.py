from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.Vector4 import Vector4


class NasutoJointEntry:

	"""
	60 bytes
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.matrix = Matrix33()
		self.vector = Vector4()

		# 1
		self.unknown_2 = 0

		# ?
		self.unknown_3_a = 0

		# ?
		self.unknown_3_b = 0

		# 0
		self.unknown_3_c = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.matrix = stream.read_type(Matrix33)
		self.vector = stream.read_type(Vector4)
		self.unknown_2 = stream.read_uint()
		self.unknown_3_a = stream.read_ubyte()
		self.unknown_3_b = stream.read_ubyte()
		self.unknown_3_c = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.matrix)
		stream.write_type(self.vector)
		stream.write_uint(self.unknown_2)
		stream.write_ubyte(self.unknown_3_a)
		stream.write_ubyte(self.unknown_3_b)
		stream.write_ushort(self.unknown_3_c)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'NasutoJointEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* matrix = ' + self.matrix.__repr__()
		s += '\n	* vector = ' + self.vector.__repr__()
		s += '\n	* unknown_2 = ' + self.unknown_2.__repr__()
		s += '\n	* unknown_3_a = ' + self.unknown_3_a.__repr__()
		s += '\n	* unknown_3_b = ' + self.unknown_3_b.__repr__()
		s += '\n	* unknown_3_c = ' + self.unknown_3_c.__repr__()
		s += '\n'
		return s
