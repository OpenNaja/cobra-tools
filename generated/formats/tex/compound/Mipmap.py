from generated.context import ContextReference


class Mipmap:

	"""
	Data struct for one mipmap, part of a data 1 struct in headers of type 7
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# starting offset into the texture buffer for this mip level
		self.offset = 0

		# bytes for one array entry
		self.size = 0

		# bytes for all array entries
		self.size_array = 0

		# size of a scan line of blocks, including padding that is added to the end of the line
		self.size_scan = 0

		# size of the non-empty scanline blocks, ie. the last lods add empty scanlines as this is smaller than size
		self.size_data = 0
		self.set_defaults()

	def set_defaults(self):
		self.offset = 0
		self.size = 0
		self.size_array = 0
		self.size_scan = 0
		self.size_data = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.offset = stream.read_uint()
		self.size = stream.read_uint()
		self.size_array = stream.read_uint()
		self.size_scan = stream.read_uint()
		self.size_data = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.offset)
		stream.write_uint(self.size)
		stream.write_uint(self.size_array)
		stream.write_uint(self.size_scan)
		stream.write_uint(self.size_data)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Mipmap [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* size = {self.size.__repr__()}'
		s += f'\n	* size_array = {self.size_array.__repr__()}'
		s += f'\n	* size_scan = {self.size_scan.__repr__()}'
		s += f'\n	* size_data = {self.size_data.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
