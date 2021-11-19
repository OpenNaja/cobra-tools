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

		# bytes
		self.size = 0

		# bytes
		self.size_repeat = 0

		# decreases quadratically
		self.unknown_0_c = 0

		# may be size of actual data - usually, repeat of size, not for the last lods
		self.unkn_3 = 0
		self.set_defaults()

	def set_defaults(self):
		self.offset = 0
		self.size = 0
		self.size_repeat = 0
		self.unknown_0_c = 0
		self.unkn_3 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.offset = stream.read_uint()
		self.size = stream.read_uint()
		self.size_repeat = stream.read_uint()
		self.unknown_0_c = stream.read_uint()
		self.unkn_3 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.offset)
		stream.write_uint(self.size)
		stream.write_uint(self.size_repeat)
		stream.write_uint(self.unknown_0_c)
		stream.write_uint(self.unkn_3)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Mipmap [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* size = {self.size.__repr__()}'
		s += f'\n	* size_repeat = {self.size_repeat.__repr__()}'
		s += f'\n	* unknown_0_c = {self.unknown_0_c.__repr__()}'
		s += f'\n	* unkn_3 = {self.unkn_3.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
