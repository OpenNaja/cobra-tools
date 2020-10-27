from generated.formats.ms2.compound.Matrix33 import Matrix33
from generated.formats.ms2.compound.Vector3 import Vector3


class BoundingBox:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.rotation = Matrix33()
		self.center = Vector3()
		self.extent = Vector3()

	def read(self, stream):

		self.io_start = stream.tell()
		self.rotation = stream.read_type(Matrix33)
		self.center = stream.read_type(Vector3)
		self.extent = stream.read_type(Vector3)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.rotation)
		stream.write_type(self.center)
		stream.write_type(self.extent)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'BoundingBox [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* rotation = ' + self.rotation.__repr__()
		s += '\n	* center = ' + self.center.__repr__()
		s += '\n	* extent = ' + self.extent.__repr__()
		s += '\n'
		return s
