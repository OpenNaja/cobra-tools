class Root1:
	flag: int
	zero_1: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.flag = 0
		self.zero_1 = 0

	def read(self, stream):

		io_start = stream.tell()
		self.flag = stream.read_uint()
		self.zero_1 = stream.read_uint()

		self.io_size = stream.tell() - io_start

	def write(self, stream):

		io_start = stream.tell()
		stream.write_uint(self.flag)
		stream.write_uint(self.zero_1)

		self.io_size = stream.tell() - io_start

	def __repr__(self):
		s = 'Root1 [Size: '+str(self.io_size)+']'
		s += '\n	* flag = ' + self.flag.__repr__()
		s += '\n	* zero_1 = ' + self.zero_1.__repr__()
		s += '\n'
		return s
