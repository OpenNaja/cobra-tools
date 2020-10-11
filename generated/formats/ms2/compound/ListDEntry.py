from generated.formats.ms2.compound.Matrix44 import Matrix44


class ListDEntry:
	ce: float
	cb: float
	matrix: Matrix44

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.ce = 0
		self.cb = 0
		self.matrix = Matrix44()

	def read(self, stream):

		self.io_start = stream.tell()
		self.ce = stream.read_float()
		self.cb = stream.read_float()
		self.matrix = stream.read_type(Matrix44)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_float(self.ce)
		stream.write_float(self.cb)
		stream.write_type(self.matrix)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'ListDEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* ce = ' + self.ce.__repr__()
		s += '\n	* cb = ' + self.cb.__repr__()
		s += '\n	* matrix = ' + self.matrix.__repr__()
		s += '\n'
		return s
