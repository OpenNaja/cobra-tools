import numpy
from generated.formats.ms2.compound.Descriptor import Descriptor


class ListFirst(Descriptor):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.floats = numpy.zeros((3), dtype=numpy.dtype('float32'))
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.floats = numpy.zeros((3), dtype=numpy.dtype('float32'))

	def read(self, stream):
		super().read(stream)
		self.floats = stream.read_floats((3))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		super().write(stream)
		stream.write_floats(self.floats)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ListFirst [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* floats = {self.floats.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
