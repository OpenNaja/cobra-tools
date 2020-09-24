class Header3Data0:

# Data struct for headers of type 3, read by data 0 of 3,7 frag.
# 16 bytes

	# 32 bytes, all 0
	zeros: int

	# flag, not direct index into DDS enum
	compression_type: int

	# 0 or 1
	one_0: int

	# 1 or 2
	one_1: int

	# 1 or 2
	one_2: int

	# 0
	pad: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.zeros = stream.read_uint64()
		self.compression_type = stream.read_ubyte()
		self.one_0 = stream.read_ubyte()
		self.one_1 = stream.read_ubyte()
		self.one_2 = stream.read_ubyte()
		self.pad = stream.read_uint()

	def write(self, stream):
		stream.write_uint64(self.zeros)
		stream.write_ubyte(self.compression_type)
		stream.write_ubyte(self.one_0)
		stream.write_ubyte(self.one_1)
		stream.write_ubyte(self.one_2)
		stream.write_uint(self.pad)

	def __repr__(self):
		s = 'Header3Data0'
		s += '\n	* zeros = ' + self.zeros.__repr__()
		s += '\n	* compression_type = ' + self.compression_type.__repr__()
		s += '\n	* one_0 = ' + self.one_0.__repr__()
		s += '\n	* one_1 = ' + self.one_1.__repr__()
		s += '\n	* one_2 = ' + self.one_2.__repr__()
		s += '\n	* pad = ' + self.pad.__repr__()
		s += '\n'
		return s