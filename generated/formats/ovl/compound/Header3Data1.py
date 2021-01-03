class Header3Data1:

	"""
	Part of a fragment, repeated for count of texture LODs / buffers.
	Data struct for headers of type 3
	24 bytes per texture buffer
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Size of previous tex buffer
		self.data_size_previous = 0
		self.zero_1 = 0

		# Size of this tex buffer
		self.data_size = 0
		self.zero_3 = 0

		# is also related to data size
		self.unkn = 0
		self.zero_5 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.data_size_previous = stream.read_uint()
		self.zero_1 = stream.read_uint()
		self.data_size = stream.read_uint()
		self.zero_3 = stream.read_uint()
		self.unkn = stream.read_uint()
		self.zero_5 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.data_size_previous)
		stream.write_uint(self.zero_1)
		stream.write_uint(self.data_size)
		stream.write_uint(self.zero_3)
		stream.write_uint(self.unkn)
		stream.write_uint(self.zero_5)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Header3Data1 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* data_size_previous = {self.data_size_previous.__repr__()}'
		s += f'\n	* zero_1 = {self.zero_1.__repr__()}'
		s += f'\n	* data_size = {self.data_size.__repr__()}'
		s += f'\n	* zero_3 = {self.zero_3.__repr__()}'
		s += f'\n	* unkn = {self.unkn.__repr__()}'
		s += f'\n	* zero_5 = {self.zero_5.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
