class HeaderEntry:

# Description of one archive header entry

	# always 0
	zeros_1: int

	# always 0
	zeros_2: int

	# the number of bytes representing the text files data
	size: int

	# starting point to read text file data
	offset: int

	# DJB hash of the first file in the txt data block
	file_hash: int

	# unknown count (number of .txt files)
	num_files: int

	# JWE: DJB hash for extension, 0 for PZ
	ext_hash: int

	# always 0
	zeros_3: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.zeros_1 = stream.read_uint()
		self.zeros_2 = stream.read_uint()
		self.size = stream.read_uint()
		self.offset = stream.read_uint()
		self.file_hash = stream.read_uint()
		self.num_files = stream.read_uint()
		self.ext_hash = stream.read_uint()
		self.zeros_3 = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.zeros_1)
		stream.write_uint(self.zeros_2)
		stream.write_uint(self.size)
		stream.write_uint(self.offset)
		stream.write_uint(self.file_hash)
		stream.write_uint(self.num_files)
		stream.write_uint(self.ext_hash)
		stream.write_uint(self.zeros_3)

	def __repr__(self):
		s = 'HeaderEntry'
		s += '\nzeros_1 ' + self.zeros_1.__repr__()
		s += '\nzeros_2 ' + self.zeros_2.__repr__()
		s += '\nsize ' + self.size.__repr__()
		s += '\noffset ' + self.offset.__repr__()
		s += '\nfile_hash ' + self.file_hash.__repr__()
		s += '\nnum_files ' + self.num_files.__repr__()
		s += '\next_hash ' + self.ext_hash.__repr__()
		s += '\nzeros_3 ' + self.zeros_3.__repr__()
		s += '\n'
		return s