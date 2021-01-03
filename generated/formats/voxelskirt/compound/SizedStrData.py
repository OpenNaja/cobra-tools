class SizedStrData:

	"""
	# JWE
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zero = 0

		# total size of buffer data
		self.data_size = 0
		self.x = 0
		self.y = 0
		self.scale = 0
		self.padding = 0
		self.data_offset = 0

		# entries of 32 bytes
		self.data_count = 0
		self.size_offset = 0

		# entries of 40 bytes
		self.size_count = 0

		# slightly smaller than total size of buffer data
		self.unk_1_offset = 0

		# counts the -1 structs; entries of 32 bytes
		self.unk_1_count = 0

		# offset into buffer to start of sth; only given if some count is nonzero
		self.unk_2_offset = 0
		self.unk_2_count = 0

		# offset into buffer to start of name zstrings
		self.name_buffer_offset = 0

		# also counts the stuff after names
		self.name_count = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.zero = stream.read_uint64()
		self.data_size = stream.read_uint64()
		self.x = stream.read_uint64()
		self.y = stream.read_uint64()
		self.scale = stream.read_float()
		self.padding = stream.read_float()
		if not (stream.version == 18):
			self.data_offset = stream.read_uint64()
			self.data_count = stream.read_uint64()
			self.size_offset = stream.read_uint64()
			self.size_count = stream.read_uint64()
		self.unk_1_offset = stream.read_uint64()
		self.unk_1_count = stream.read_uint64()
		self.unk_2_offset = stream.read_uint64()
		self.unk_2_count = stream.read_uint64()
		self.name_buffer_offset = stream.read_uint64()
		self.name_count = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.zero)
		stream.write_uint64(self.data_size)
		stream.write_uint64(self.x)
		stream.write_uint64(self.y)
		stream.write_float(self.scale)
		stream.write_float(self.padding)
		if not (stream.version == 18):
			stream.write_uint64(self.data_offset)
			stream.write_uint64(self.data_count)
			stream.write_uint64(self.size_offset)
			stream.write_uint64(self.size_count)
		stream.write_uint64(self.unk_1_offset)
		stream.write_uint64(self.unk_1_count)
		stream.write_uint64(self.unk_2_offset)
		stream.write_uint64(self.unk_2_count)
		stream.write_uint64(self.name_buffer_offset)
		stream.write_uint64(self.name_count)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'SizedStrData [Size: '+str(self.io_size)+', Address: '+str(self.io_start)+'] ' + self.name
		s += '\n	* zero = ' + self.zero.__repr__()
		s += '\n	* data_size = ' + self.data_size.__repr__()
		s += '\n	* x = ' + self.x.__repr__()
		s += '\n	* y = ' + self.y.__repr__()
		s += '\n	* scale = ' + self.scale.__repr__()
		s += '\n	* padding = ' + self.padding.__repr__()
		s += '\n	* data_offset = ' + self.data_offset.__repr__()
		s += '\n	* data_count = ' + self.data_count.__repr__()
		s += '\n	* size_offset = ' + self.size_offset.__repr__()
		s += '\n	* size_count = ' + self.size_count.__repr__()
		s += '\n	* unk_1_offset = ' + self.unk_1_offset.__repr__()
		s += '\n	* unk_1_count = ' + self.unk_1_count.__repr__()
		s += '\n	* unk_2_offset = ' + self.unk_2_offset.__repr__()
		s += '\n	* unk_2_count = ' + self.unk_2_count.__repr__()
		s += '\n	* name_buffer_offset = ' + self.name_buffer_offset.__repr__()
		s += '\n	* name_count = ' + self.name_count.__repr__()
		s += '\n'
		return s
