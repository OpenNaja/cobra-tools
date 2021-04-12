from generated.formats.ms2.compound.Capsule import Capsule


class Cylinder(Capsule):

	"""
	identical data to capsule, just imported differently
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		super().__init__(arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

	def read(self, stream):

		self.io_start = stream.tell()
		super().read(stream)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		super().write(stream)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Cylinder [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
