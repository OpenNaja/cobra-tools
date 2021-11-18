import numpy
from generated.array import Array
from generated.context import ContextReference


class Matrix44:

	"""
	A 4x4 transformation matrix.
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Stored in OpenGL column-major format.
		self.data = numpy.zeros((4, 4), dtype='float')
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.data = numpy.zeros((4, 4), dtype='float')

	def read(self, stream):
		self.io_start = stream.tell()
		self.data = stream.read_floats((4, 4))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_floats(self.data)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Matrix44 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* data = {self.data.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s

	def set_rows(self, mat):
		"""Set matrix from rows."""
		self.data[:] = mat.transposed()

