from generated.formats.ms2.compound.Matrix33 import Matrix33


class ListCEntry:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 1 for carch and nasuto
		self.one = 0
		self.matrix = Matrix33()
		self.a = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.one = stream.read_uint()
		self.matrix = stream.read_type(Matrix33)
		self.a = stream.read_float()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.one)
		stream.write_type(self.matrix)
		stream.write_float(self.a)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ListCEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* one = {self.one.__repr__()}'
		s += f'\n	* matrix = {self.matrix.__repr__()}'
		s += f'\n	* a = {self.a.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
