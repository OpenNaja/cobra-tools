class Data:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.id = 0
		self.type = 0
		self.offset = 0
		self.dsize = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.id = stream.read_uint64()
		self.type = stream.read_uint64()
		self.offset = stream.read_uint64()
		self.dsize = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.id)
		stream.write_uint64(self.type)
		stream.write_uint64(self.offset)
		stream.write_uint64(self.dsize)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Data [Size: '+str(self.io_size)+', Address: '+str(self.io_start)+'] ' + self.name
		s += '\n	* id = ' + self.id.__repr__()
		s += '\n	* type = ' + self.type.__repr__()
		s += '\n	* offset = ' + self.offset.__repr__()
		s += '\n	* dsize = ' + self.dsize.__repr__()
		s += '\n'
		return s
