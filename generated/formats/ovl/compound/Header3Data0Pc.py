from generated.formats.ovl.enum.DdsTypeCoaster import DdsTypeCoaster


class Header3Data0Pc:

	"""
	Data struct for headers of type 3, read by data 0 of 3,7 frag.
	16 bytes
	"""

	# 32 bytes, all 0
	zeros: int

	# flag, not direct index into DDS enum
	compression_type: DdsTypeCoaster

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
		self.io_size = 0
		self.io_start = 0
		self.zeros = 0
		self.compression_type = DdsTypeCoaster()
		self.one_0 = 0
		self.one_1 = 0
		self.one_2 = 0
		self.pad = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.zeros = stream.read_uint64()
		self.compression_type = DdsTypeCoaster(stream.read_ubyte())
		self.one_0 = stream.read_ubyte()
		self.one_1 = stream.read_ubyte()
		self.one_2 = stream.read_ubyte()
		self.pad = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.zeros)
		stream.write_ubyte(self.compression_type.value)
		stream.write_ubyte(self.one_0)
		stream.write_ubyte(self.one_1)
		stream.write_ubyte(self.one_2)
		stream.write_uint(self.pad)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Header3Data0Pc [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* zeros = ' + self.zeros.__repr__()
		s += '\n	* compression_type = ' + self.compression_type.__repr__()
		s += '\n	* one_0 = ' + self.one_0.__repr__()
		s += '\n	* one_1 = ' + self.one_1.__repr__()
		s += '\n	* one_2 = ' + self.one_2.__repr__()
		s += '\n	* pad = ' + self.pad.__repr__()
		s += '\n'
		return s
