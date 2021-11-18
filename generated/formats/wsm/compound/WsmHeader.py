import numpy
from generated.array import Array
from generated.context import ContextReference


class WsmHeader:

	"""
	40 bytes for JWE2
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.duration = 0

		# likely
		self.frame_count = 0

		# unk
		self.unknowns = numpy.zeros((8), dtype='float')
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.duration = 0
		self.frame_count = 0
		self.unknowns = numpy.zeros((8), dtype='float')

	def read(self, stream):
		self.io_start = stream.tell()
		self.duration = stream.read_float()
		self.frame_count = stream.read_uint()
		self.unknowns = stream.read_floats((8))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_float(self.duration)
		stream.write_uint(self.frame_count)
		stream.write_floats(self.unknowns)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'WsmHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* duration = {self.duration.__repr__()}'
		s += f'\n	* frame_count = {self.frame_count.__repr__()}'
		s += f'\n	* unknowns = {self.unknowns.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
