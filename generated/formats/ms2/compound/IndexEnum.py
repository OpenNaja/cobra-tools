class IndexEnum:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.four = 0

		# linear increase
		self.index = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.four = stream.read_uint()
		self.index = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.four)
		stream.write_uint(self.index)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'IndexEnum [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* four = {self.four.__repr__()}'
		s += f'\n	* index = {self.index.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
