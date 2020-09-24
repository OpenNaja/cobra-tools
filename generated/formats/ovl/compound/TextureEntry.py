class TextureEntry:

# Description of one texture

	# Hash of this texture, for lookup in hash dict.
	file_hash: int
	unknown_1: int
	unknown_2: int
	unknown_3: int
	unknown_4: int
	unknown_5: int
	unknown_6: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.file_hash = stream.read_uint()
		self.unknown_1 = stream.read_uint()
		self.unknown_2 = stream.read_ubyte()
		self.unknown_3 = stream.read_ubyte()
		self.unknown_4 = stream.read_ushort()
		self.unknown_5 = stream.read_uint()
		self.unknown_6 = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.file_hash)
		stream.write_uint(self.unknown_1)
		stream.write_ubyte(self.unknown_2)
		stream.write_ubyte(self.unknown_3)
		stream.write_ushort(self.unknown_4)
		stream.write_uint(self.unknown_5)
		stream.write_uint(self.unknown_6)

	def __repr__(self):
		s = 'TextureEntry'
		s += '\n	* file_hash = ' + self.file_hash.__repr__()
		s += '\n	* unknown_1 = ' + self.unknown_1.__repr__()
		s += '\n	* unknown_2 = ' + self.unknown_2.__repr__()
		s += '\n	* unknown_3 = ' + self.unknown_3.__repr__()
		s += '\n	* unknown_4 = ' + self.unknown_4.__repr__()
		s += '\n	* unknown_5 = ' + self.unknown_5.__repr__()
		s += '\n	* unknown_6 = ' + self.unknown_6.__repr__()
		s += '\n'
		return s