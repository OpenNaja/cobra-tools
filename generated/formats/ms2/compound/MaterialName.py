import typing


class MaterialName:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index into ms2 names array
		self.name_index = 0

		# index into ms2 names array
		self.name_index = 0

		# unknown, nonzero in PZ flamingo juvenile, might be junk (padding)
		self.some_index = 0

		# unknown, nonzero in PZ flamingo juvenile, might be junk (padding)
		self.some_index = 0

	def read(self, stream):

		self.io_start = stream.tell()
		if not (stream.version < 19):
			self.name_index = stream.read_uint()
		if stream.version < 19:
			self.name_index = stream.read_ushort()
		if not (stream.version < 19):
			self.some_index = stream.read_uint()
		if stream.version < 19:
			self.some_index = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		if not (stream.version < 19):
			stream.write_uint(self.name_index)
		if stream.version < 19:
			stream.write_ushort(self.name_index)
		if not (stream.version < 19):
			stream.write_uint(self.some_index)
		if stream.version < 19:
			stream.write_ushort(self.some_index)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'MaterialName [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* name_index = {self.name_index.__repr__()}'
		s += f'\n	* some_index = {self.some_index.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
