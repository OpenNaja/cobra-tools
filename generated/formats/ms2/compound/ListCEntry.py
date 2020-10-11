from generated.formats.ms2.compound.Matrix33 import Matrix33


class ListCEntry:

	# 1 for carch and nasuto
	one: int
	matrix: Matrix33
	a: float

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.one = 0
		self.matrix = Matrix33()
		self.a = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.one = stream.read_uint()
		self.matrix = stream.read_type(Matrix33)
		self.a = stream.read_float()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.one)
		stream.write_type(self.matrix)
		stream.write_float(self.a)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'ListCEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* one = ' + self.one.__repr__()
		s += '\n	* matrix = ' + self.matrix.__repr__()
		s += '\n	* a = ' + self.a.__repr__()
		s += '\n'
		return s
