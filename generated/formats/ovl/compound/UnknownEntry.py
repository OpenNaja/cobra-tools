class UnknownEntry:

	"""
	Description of one file type
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.unknown_1 = 0
		self.unknown_2 = 0
		self.unknown_3 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.unknown_1 = stream.read_uint()
		self.unknown_2 = stream.read_uint()
		self.unknown_3 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.unknown_1)
		stream.write_uint(self.unknown_2)
		stream.write_uint(self.unknown_3)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'UnknownEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* unknown_1 = {self.unknown_1.__repr__()}'
		s += f'\n	* unknown_2 = {self.unknown_2.__repr__()}'
		s += f'\n	* unknown_3 = {self.unknown_3.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
