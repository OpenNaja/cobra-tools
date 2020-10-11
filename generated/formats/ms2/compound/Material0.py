class Material0:
	a: int
	b: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.a = 0
		self.b = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.a = stream.read_uint()
		self.b = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.a)
		stream.write_uint(self.b)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Material0 [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* a = ' + self.a.__repr__()
		s += '\n	* b = ' + self.b.__repr__()
		s += '\n'
		return s
