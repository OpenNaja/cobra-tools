class DataEntry:

# 32 bytes

	# DJB hash; sometimes matches an archive header's first File Hash
	file_hash: int

	# DJB hash for extension; always (?) matches an archive header's hash
	ext_hash: int
	set_index: int

	# number of buffers that should be read from list for this entry
	buffer_count: int
	zero_10: int

	# size of first buffer, in the case of the ms2 the size 1 is the sizw of the first two buffers together
	size_1: int
	zero_18: int

	# size of last buffer
	size_2: int
	zero_20: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.file_hash = stream.read_uint()
		self.ext_hash = stream.read_uint()
		self.set_index = stream.read_ushort()
		self.buffer_count = stream.read_ushort()
		self.zero_10 = stream.read_uint()
		self.size_1 = stream.read_uint()
		self.zero_18 = stream.read_uint()
		self.size_2 = stream.read_uint()
		self.zero_20 = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.file_hash)
		stream.write_uint(self.ext_hash)
		stream.write_ushort(self.set_index)
		stream.write_ushort(self.buffer_count)
		stream.write_uint(self.zero_10)
		stream.write_uint(self.size_1)
		stream.write_uint(self.zero_18)
		stream.write_uint(self.size_2)
		stream.write_uint(self.zero_20)

	def __repr__(self):
		s = 'DataEntry'
		s += '\nfile_hash ' + self.file_hash.__repr__()
		s += '\next_hash ' + self.ext_hash.__repr__()
		s += '\nset_index ' + self.set_index.__repr__()
		s += '\nbuffer_count ' + self.buffer_count.__repr__()
		s += '\nzero_10 ' + self.zero_10.__repr__()
		s += '\nsize_1 ' + self.size_1.__repr__()
		s += '\nzero_18 ' + self.zero_18.__repr__()
		s += '\nsize_2 ' + self.size_2.__repr__()
		s += '\nzero_20 ' + self.zero_20.__repr__()
		s += '\n'
		return s