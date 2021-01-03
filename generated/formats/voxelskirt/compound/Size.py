class Size:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.id = 0
		self.width_1 = 0
		self.height_1 = 0
		self.width_2 = 0
		self.height_2 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.id = stream.read_uint64()
		self.width_1 = stream.read_uint64()
		self.height_1 = stream.read_uint64()
		self.width_2 = stream.read_uint64()
		self.height_2 = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.id)
		stream.write_uint64(self.width_1)
		stream.write_uint64(self.height_1)
		stream.write_uint64(self.width_2)
		stream.write_uint64(self.height_2)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Size [Size: '+str(self.io_size)+', Address: '+str(self.io_start)+'] ' + self.name
		s += '\n	* id = ' + self.id.__repr__()
		s += '\n	* width_1 = ' + self.width_1.__repr__()
		s += '\n	* height_1 = ' + self.height_1.__repr__()
		s += '\n	* width_2 = ' + self.width_2.__repr__()
		s += '\n	* height_2 = ' + self.height_2.__repr__()
		s += '\n'
		return s
