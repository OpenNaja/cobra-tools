class TextureInfo:

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zero_0 = 0
		self.zero_1 = 0
		self.texture_count = 0
		self.zero_4 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.zero_0 = stream.read_uint()
		self.zero_1 = stream.read_uint()
		self.texture_count = stream.read_uint()
		self.zero_4 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.zero_0)
		stream.write_uint(self.zero_1)
		stream.write_uint(self.texture_count)
		stream.write_uint(self.zero_4)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'TextureInfo [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* zero_0 = ' + self.zero_0.__repr__()
		s += '\n	* zero_1 = ' + self.zero_1.__repr__()
		s += '\n	* texture_count = ' + self.texture_count.__repr__()
		s += '\n	* zero_4 = ' + self.zero_4.__repr__()
		s += '\n'
		return s
