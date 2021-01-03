class PosInfo:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.offset = 0
		self.count = 0
		self.id = 0
		self.ff = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.offset = stream.read_uint64()
		self.count = stream.read_uint64()
		self.id = stream.read_uint64()
		self.ff = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.offset)
		stream.write_uint64(self.count)
		stream.write_uint64(self.id)
		stream.write_uint64(self.ff)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'PosInfo [Size: '+str(self.io_size)+', Address: '+str(self.io_start)+'] ' + self.name
		s += '\n	* offset = ' + self.offset.__repr__()
		s += '\n	* count = ' + self.count.__repr__()
		s += '\n	* id = ' + self.id.__repr__()
		s += '\n	* ff = ' + self.ff.__repr__()
		s += '\n'
		return s
