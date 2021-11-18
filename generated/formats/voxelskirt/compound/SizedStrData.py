from generated.context import ContextReference


class SizedStrData:

	"""
	# size varies according to game
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
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

		# zero, for PC only
		self.zero_pc = 0

		# x*y*4, for PC only
		self.height_array_size_pc = 0
		self.data_offset = 0

		# entries of 32 bytes
		self.data_count = 0
		self.size_offset = 0

		# entries of 40 bytes
		self.size_count = 0

		# slightly smaller than total size of buffer data
		self.position_offset = 0

		# counts the -1 structs; entries of 32 bytes
		self.position_count = 0

		# offset into buffer to start of sth; only given if some count is nonzero
		self.mat_offset = 0
		self.mat_count = 0

		# offset into buffer to start of name zstrings
		self.name_buffer_offset = 0

		# also counts the stuff after names
		self.name_count = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.zero = 0
		self.data_size = 0
		self.x = 0
		self.y = 0
		self.scale = 0
		self.padding = 0
		if self.context.version == 18:
			self.zero_pc = 0
		if self.context.version == 18:
			self.height_array_size_pc = 0
		if not (self.context.version == 18):
			self.data_offset = 0
		if not (self.context.version == 18):
			self.data_count = 0
		if not (self.context.version == 18):
			self.size_offset = 0
		if not (self.context.version == 18):
			self.size_count = 0
		self.position_offset = 0
		self.position_count = 0
		self.mat_offset = 0
		self.mat_count = 0
		self.name_buffer_offset = 0
		self.name_count = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.zero = stream.read_uint64()
		self.data_size = stream.read_uint64()
		self.x = stream.read_uint64()
		self.y = stream.read_uint64()
		self.scale = stream.read_float()
		self.padding = stream.read_float()
		if self.context.version == 18:
			self.zero_pc = stream.read_uint64()
			self.height_array_size_pc = stream.read_uint64()
		if not (self.context.version == 18):
			self.data_offset = stream.read_uint64()
			self.data_count = stream.read_uint64()
		if not (self.context.version == 18):
			self.size_offset = stream.read_uint64()
			self.size_count = stream.read_uint64()
		self.position_offset = stream.read_uint64()
		self.position_count = stream.read_uint64()
		self.mat_offset = stream.read_uint64()
		self.mat_count = stream.read_uint64()
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
		if self.context.version == 18:
			stream.write_uint64(self.zero_pc)
			stream.write_uint64(self.height_array_size_pc)
		if not (self.context.version == 18):
			stream.write_uint64(self.data_offset)
			stream.write_uint64(self.data_count)
		if not (self.context.version == 18):
			stream.write_uint64(self.size_offset)
			stream.write_uint64(self.size_count)
		stream.write_uint64(self.position_offset)
		stream.write_uint64(self.position_count)
		stream.write_uint64(self.mat_offset)
		stream.write_uint64(self.mat_count)
		stream.write_uint64(self.name_buffer_offset)
		stream.write_uint64(self.name_count)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'SizedStrData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* data_size = {self.data_size.__repr__()}'
		s += f'\n	* x = {self.x.__repr__()}'
		s += f'\n	* y = {self.y.__repr__()}'
		s += f'\n	* scale = {self.scale.__repr__()}'
		s += f'\n	* padding = {self.padding.__repr__()}'
		s += f'\n	* zero_pc = {self.zero_pc.__repr__()}'
		s += f'\n	* height_array_size_pc = {self.height_array_size_pc.__repr__()}'
		s += f'\n	* data_offset = {self.data_offset.__repr__()}'
		s += f'\n	* data_count = {self.data_count.__repr__()}'
		s += f'\n	* size_offset = {self.size_offset.__repr__()}'
		s += f'\n	* size_count = {self.size_count.__repr__()}'
		s += f'\n	* position_offset = {self.position_offset.__repr__()}'
		s += f'\n	* position_count = {self.position_count.__repr__()}'
		s += f'\n	* mat_offset = {self.mat_offset.__repr__()}'
		s += f'\n	* mat_count = {self.mat_count.__repr__()}'
		s += f'\n	* name_buffer_offset = {self.name_buffer_offset.__repr__()}'
		s += f'\n	* name_count = {self.name_count.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
