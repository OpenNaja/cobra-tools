class EnumnamerStrData:

	"""
	per attribute
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 3 in driver
		self.unknown_0 = 0

		# 0 in driver
		self.unknown_1 = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.unknown_0 = stream.read_uint()
		self.unknown_1 = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.unknown_0)
		stream.write_uint(self.unknown_1)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'EnumnamerStrData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* unknown_0 = {self.unknown_0.__repr__()}'
		s += f'\n	* unknown_1 = {self.unknown_1.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
