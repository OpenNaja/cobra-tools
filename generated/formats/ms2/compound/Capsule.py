from generated.formats.ms2.compound.Vector3 import Vector3


class Capsule:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.a = Vector3()
		self.b = Vector3()
		self.c = Vector3()

	def read(self, stream):

		self.io_start = stream.tell()
		self.a = stream.read_type(Vector3)
		self.b = stream.read_type(Vector3)
		self.c = stream.read_type(Vector3)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.a)
		stream.write_type(self.b)
		stream.write_type(self.c)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Capsule [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* a = {self.a.__repr__()}'
		s += f'\n	* b = {self.b.__repr__()}'
		s += f'\n	* c = {self.c.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
