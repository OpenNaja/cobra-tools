class TwoFragFgmExtra:
	zero_3: int
	zero_4: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.zero_3 = 0
		self.zero_4 = 0

	def read(self, stream):

		io_start = stream.tell()
		self.zero_3 = stream.read_uint()
		self.zero_4 = stream.read_uint()

		self.io_size = stream.tell() - io_start

	def write(self, stream):

		io_start = stream.tell()
		stream.write_uint(self.zero_3)
		stream.write_uint(self.zero_4)

		self.io_size = stream.tell() - io_start

	def __repr__(self):
		s = 'TwoFragFgmExtra [Size: '+str(self.io_size)+']'
		s += '\n	* zero_3 = ' + self.zero_3.__repr__()
		s += '\n	* zero_4 = ' + self.zero_4.__repr__()
		s += '\n'
		return s
