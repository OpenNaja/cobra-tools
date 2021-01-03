from generated.formats.ms2.compound.Matrix44 import Matrix44


class ListDEntry:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.ce = 0
		self.cb = 0
		self.matrix = Matrix44()

	def read(self, stream):

		self.io_start = stream.tell()
		self.ce = stream.read_float()
		self.cb = stream.read_float()
		self.matrix = stream.read_type(Matrix44)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_float(self.ce)
		stream.write_float(self.cb)
		stream.write_type(self.matrix)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ListDEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* ce = {self.ce.__repr__()}'
		s += f'\n	* cb = {self.cb.__repr__()}'
		s += f'\n	* matrix = {self.matrix.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
