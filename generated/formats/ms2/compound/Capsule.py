from generated.formats.ms2.compound.Vector3 import Vector3


class Capsule:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.a = Vector3()
		self.b = Vector3()
		self.c = Vector3()

	def read(self, stream):

		self.io_start = stream.tell()
		self.a = stream.read_type(Vector3)
		self.b = stream.read_type(Vector3)
		self.c = stream.read_type(Vector3)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.a)
		stream.write_type(self.b)
		stream.write_type(self.c)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Capsule [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* a = ' + self.a.__repr__()
		s += '\n	* b = ' + self.b.__repr__()
		s += '\n	* c = ' + self.c.__repr__()
		s += '\n'
		return s
