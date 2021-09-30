from generated.context import ContextReference
from generated.formats.ms2.compound.Vector3 import Vector3


class Sphere:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# center of the sphere
		self.center = Vector3(context, None, None)

		# radius around the center
		self.radius = 0

		# apparently unused
		self.zero = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.center = stream.read_type(Vector3)
		self.radius = stream.read_float()
		self.zero = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.center)
		stream.write_float(self.radius)
		stream.write_uint(self.zero)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Sphere [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* center = {self.center.__repr__()}'
		s += f'\n	* radius = {self.radius.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
