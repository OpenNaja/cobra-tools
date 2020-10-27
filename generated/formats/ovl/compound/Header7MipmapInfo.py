class Header7MipmapInfo:

	"""
	Data struct for one mipmap, part of a data 1 struct in headers of type 7
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.offset = 0
		self.unknown_02 = 0
		self.width = 0
		self.height = 0
		self.unknown_0_c = 0
		self.unkn_3 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.offset = stream.read_ushort()
		self.unknown_02 = stream.read_ushort()
		self.width = stream.read_uint()
		self.height = stream.read_uint()
		self.unknown_0_c = stream.read_uint()
		self.unkn_3 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushort(self.offset)
		stream.write_ushort(self.unknown_02)
		stream.write_uint(self.width)
		stream.write_uint(self.height)
		stream.write_uint(self.unknown_0_c)
		stream.write_uint(self.unkn_3)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Header7MipmapInfo [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* offset = ' + self.offset.__repr__()
		s += '\n	* unknown_02 = ' + self.unknown_02.__repr__()
		s += '\n	* width = ' + self.width.__repr__()
		s += '\n	* height = ' + self.height.__repr__()
		s += '\n	* unknown_0_c = ' + self.unknown_0_c.__repr__()
		s += '\n	* unkn_3 = ' + self.unkn_3.__repr__()
		s += '\n'
		return s
