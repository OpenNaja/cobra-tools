class BufferEndData:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# in bytes
		self.size_of_height_and_weights = 0
		self.unk = 0
		self.index = 0
		self.ff = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.size_of_height_and_weights = stream.read_uint64()
		self.unk = stream.read_uint64()
		self.index = stream.read_uint64()
		self.ff = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.size_of_height_and_weights)
		stream.write_uint64(self.unk)
		stream.write_uint64(self.index)
		stream.write_uint64(self.ff)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'BufferEndData [Size: '+str(self.io_size)+', Address: '+str(self.io_start)+'] ' + self.name
		s += '\n	* size_of_height_and_weights = ' + self.size_of_height_and_weights.__repr__()
		s += '\n	* unk = ' + self.unk.__repr__()
		s += '\n	* index = ' + self.index.__repr__()
		s += '\n	* ff = ' + self.ff.__repr__()
		s += '\n'
		return s
