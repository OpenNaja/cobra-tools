from generated.formats.ms2.compound.Vector3 import Vector3


class Sphere:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.center = Vector3()
		self.radius = 0
		self.unk = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.center = stream.read_type(Vector3)
		self.radius = stream.read_float()
		self.unk = stream.read_float()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.center)
		stream.write_float(self.radius)
		stream.write_float(self.unk)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Sphere [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* center = ' + self.center.__repr__()
		s += '\n	* radius = ' + self.radius.__repr__()
		s += '\n	* unk = ' + self.unk.__repr__()
		s += '\n'
		return s
