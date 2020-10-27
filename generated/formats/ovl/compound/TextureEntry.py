class TextureEntry:

	"""
	Description of one texture
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Hash of this texture, for lookup in hash dict.
		self.file_hash = 0
		self.unknown_1 = 0
		self.unknown_2 = 0
		self.unknown_3 = 0
		self.unknown_4 = 0
		self.unknown_5 = 0
		self.unknown_6 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.file_hash = stream.read_uint()
		self.unknown_1 = stream.read_uint()
		self.unknown_2 = stream.read_ubyte()
		self.unknown_3 = stream.read_ubyte()
		self.unknown_4 = stream.read_ushort()
		self.unknown_5 = stream.read_uint()
		self.unknown_6 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.file_hash)
		stream.write_uint(self.unknown_1)
		stream.write_ubyte(self.unknown_2)
		stream.write_ubyte(self.unknown_3)
		stream.write_ushort(self.unknown_4)
		stream.write_uint(self.unknown_5)
		stream.write_uint(self.unknown_6)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'TextureEntry [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* file_hash = ' + self.file_hash.__repr__()
		s += '\n	* unknown_1 = ' + self.unknown_1.__repr__()
		s += '\n	* unknown_2 = ' + self.unknown_2.__repr__()
		s += '\n	* unknown_3 = ' + self.unknown_3.__repr__()
		s += '\n	* unknown_4 = ' + self.unknown_4.__repr__()
		s += '\n	* unknown_5 = ' + self.unknown_5.__repr__()
		s += '\n	* unknown_6 = ' + self.unknown_6.__repr__()
		s += '\n'
		return s
