class Header7MipmapInfo:

# Data struct for one mipmap, part of a data 1 struct in headers of type 7
	offset: int
	unknown_02: int
	width: int
	height: int
	unknown_0_c: int
	unkn_3: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.offset = stream.read_ushort()
		self.unknown_02 = stream.read_ushort()
		self.width = stream.read_uint()
		self.height = stream.read_uint()
		self.unknown_0_c = stream.read_uint()
		self.unkn_3 = stream.read_uint()

	def write(self, stream):
		stream.write_ushort(self.offset)
		stream.write_ushort(self.unknown_02)
		stream.write_uint(self.width)
		stream.write_uint(self.height)
		stream.write_uint(self.unknown_0_c)
		stream.write_uint(self.unkn_3)

	def __repr__(self):
		s = 'Header7MipmapInfo'
		s += '\n	* offset = ' + self.offset.__repr__()
		s += '\n	* unknown_02 = ' + self.unknown_02.__repr__()
		s += '\n	* width = ' + self.width.__repr__()
		s += '\n	* height = ' + self.height.__repr__()
		s += '\n	* unknown_0_c = ' + self.unknown_0_c.__repr__()
		s += '\n	* unkn_3 = ' + self.unkn_3.__repr__()
		s += '\n'
		return s