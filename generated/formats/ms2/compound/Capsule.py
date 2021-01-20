from generated.formats.ms2.compound.Vector3 import Vector3


class Capsule:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.offset = Vector3()

		# normalized
		self.direction = Vector3()
		self.radius = 0
		self.extent = 0

		# apparently unused
		self.zero = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.offset = stream.read_type(Vector3)
		self.direction = stream.read_type(Vector3)
		self.radius = stream.read_float()
		self.extent = stream.read_float()
		self.zero = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.offset)
		stream.write_type(self.direction)
		stream.write_float(self.radius)
		stream.write_float(self.extent)
		stream.write_uint(self.zero)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Capsule [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* direction = {self.direction.__repr__()}'
		s += f'\n	* radius = {self.radius.__repr__()}'
		s += f'\n	* extent = {self.extent.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
