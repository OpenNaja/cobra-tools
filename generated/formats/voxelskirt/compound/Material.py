class Material:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# address of child data
		self.offset = 0

		# repeat count of child structs (4 floats)
		self.count = 0

		# index into name list
		self.id = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.offset = stream.read_uint64()
		self.count = stream.read_uint64()
		self.id = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.offset)
		stream.write_uint64(self.count)
		stream.write_uint64(self.id)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Material [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* count = {self.count.__repr__()}'
		s += f'\n	* id = {self.id.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
