from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.Vector3 import Vector3


class JointEntry:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.matrix = Matrix33()
		self.vector = Vector3()

	def read(self, stream):

		self.io_start = stream.tell()
		self.matrix = stream.read_type(Matrix33)
		self.vector = stream.read_type(Vector3)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.matrix)
		stream.write_type(self.vector)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'JointEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* matrix = ' + self.matrix.__repr__()
		s += '\n	* vector = ' + self.vector.__repr__()
		s += '\n'
		return s
