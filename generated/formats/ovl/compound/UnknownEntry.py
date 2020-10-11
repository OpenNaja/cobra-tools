class UnknownEntry:

	"""
	Description of one file type
	"""
	unknown_1: int
	unknown_2: int
	unknown_3: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.unknown_1 = 0
		self.unknown_2 = 0
		self.unknown_3 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.unknown_1 = stream.read_uint()
		self.unknown_2 = stream.read_uint()
		self.unknown_3 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.unknown_1)
		stream.write_uint(self.unknown_2)
		stream.write_uint(self.unknown_3)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'UnknownEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* unknown_1 = ' + self.unknown_1.__repr__()
		s += '\n	* unknown_2 = ' + self.unknown_2.__repr__()
		s += '\n	* unknown_3 = ' + self.unknown_3.__repr__()
		s += '\n'
		return s
