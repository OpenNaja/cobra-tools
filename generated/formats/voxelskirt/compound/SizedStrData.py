class SizedStrData:

	"""
	# 104 bytes
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
		self.height = 0
		self.zero_float = 0

		# zero, for PC only
		self.zero_pc = 0

		# x*y*4, for PC only
		self.height_array_size_pc = 0
		self.extra_offset = 0

		# entries of 32 bytes
		self.extra_count = 0
		self.another_offset = 0

		# entries of 40 bytes
		self.another_count = 0

		# slightly smaller than total size of buffer data
		self.data_offset = 0

		# counts the -1 structs; entries of 32 bytes
		self.data_count = 0

		# offset into buffer to start of sth; only given if some count is nonzero
		self.some_offset = 0
		self.some_count = 0

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
		self.height = stream.read_float()
		self.zero_float = stream.read_float()
		if stream.version == 18:
			self.zero_pc = stream.read_uint64()
			self.height_array_size_pc = stream.read_uint64()
		if not (stream.version == 18):
			self.extra_offset = stream.read_uint64()
			self.extra_count = stream.read_uint64()
			self.another_offset = stream.read_uint64()
			self.another_count = stream.read_uint64()
		self.data_offset = stream.read_uint64()
		self.data_count = stream.read_uint64()
		self.some_offset = stream.read_uint64()
		self.some_count = stream.read_uint64()
		self.name_buffer_offset = stream.read_uint64()
		self.name_count = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.zero)
		stream.write_uint64(self.data_size)
		stream.write_uint64(self.x)
		stream.write_uint64(self.y)
		stream.write_float(self.height)
		stream.write_float(self.zero_float)
		if stream.version == 18:
			stream.write_uint64(self.zero_pc)
			stream.write_uint64(self.height_array_size_pc)
		if not (stream.version == 18):
			stream.write_uint64(self.extra_offset)
			stream.write_uint64(self.extra_count)
			stream.write_uint64(self.another_offset)
			stream.write_uint64(self.another_count)
		stream.write_uint64(self.data_offset)
		stream.write_uint64(self.data_count)
		stream.write_uint64(self.some_offset)
		stream.write_uint64(self.some_count)
		stream.write_uint64(self.name_buffer_offset)
		stream.write_uint64(self.name_count)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'SizedStrData [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+'] ' + self.name
		s += '\n	* zero = ' + self.zero.__repr__()
		s += '\n	* data_size = ' + self.data_size.__repr__()
		s += '\n	* x = ' + self.x.__repr__()
		s += '\n	* y = ' + self.y.__repr__()
		s += '\n	* height = ' + self.height.__repr__()
		s += '\n	* zero_float = ' + self.zero_float.__repr__()
		s += '\n	* zero_pc = ' + self.zero_pc.__repr__()
		s += '\n	* height_array_size_pc = ' + self.height_array_size_pc.__repr__()
		s += '\n	* extra_offset = ' + self.extra_offset.__repr__()
		s += '\n	* extra_count = ' + self.extra_count.__repr__()
		s += '\n	* another_offset = ' + self.another_offset.__repr__()
		s += '\n	* another_count = ' + self.another_count.__repr__()
		s += '\n	* data_offset = ' + self.data_offset.__repr__()
		s += '\n	* data_count = ' + self.data_count.__repr__()
		s += '\n	* some_offset = ' + self.some_offset.__repr__()
		s += '\n	* some_count = ' + self.some_count.__repr__()
		s += '\n	* name_buffer_offset = ' + self.name_buffer_offset.__repr__()
		s += '\n	* name_count = ' + self.name_count.__repr__()
		s += '\n'
		return s
