from generated.formats.ms2.compound.Capsule import Capsule


class Cylinder(Capsule):

	"""
	identical data to capsule, just imported differently
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		pass

	def read(self, stream):
		super().read(stream)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
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
