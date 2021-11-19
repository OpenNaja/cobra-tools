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

		# decreases quadratically
		self.unknown = 0

		# may be size of actual data - usually, repeat of size, not for the last lods
		self.size_2 = 0
		self.set_defaults()

	def set_defaults(self):
		self.offset = 0
		self.size = 0
		self.size_array = 0
		self.unknown = 0
		self.size_2 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.offset = stream.read_uint()
		self.size = stream.read_uint()
		self.size_array = stream.read_uint()
		self.unknown = stream.read_uint()
		self.size_2 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.offset)
		stream.write_uint(self.size)
		stream.write_uint(self.size_array)
		stream.write_uint(self.unknown)
		stream.write_uint(self.size_2)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Mipmap [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* size = {self.size.__repr__()}'
		s += f'\n	* size_array = {self.size_array.__repr__()}'
		s += f'\n	* unknown = {self.unknown.__repr__()}'
		s += f'\n	* size_2 = {self.size_2.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
