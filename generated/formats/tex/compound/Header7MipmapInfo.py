class Header7MipmapInfo:

	"""
	Data struct for one mipmap, part of a data 1 struct in headers of type 7
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# cumulative sum of the preceding values
		self.offset = 0

		# not pixels
		self.width = 0

		# not pixels
		self.height = 0

		# decreases quadratically
		self.unknown_0_c = 0

		# repeat of height or width
		self.unkn_3 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.offset = stream.read_uint()
		self.width = stream.read_uint()
		self.height = stream.read_uint()
		self.unknown_0_c = stream.read_uint()
		self.unkn_3 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.offset)
		stream.write_uint(self.width)
		stream.write_uint(self.height)
		stream.write_uint(self.unknown_0_c)
		stream.write_uint(self.unkn_3)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Header7MipmapInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* width = {self.width.__repr__()}'
		s += f'\n	* height = {self.height.__repr__()}'
		s += f'\n	* unknown_0_c = {self.unknown_0_c.__repr__()}'
		s += f'\n	* unkn_3 = {self.unkn_3.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
