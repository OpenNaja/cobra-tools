import numpy
from generated.array import Array
from generated.context import ContextReference


class SizedString:

	"""
	A string of given length.
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# The string length.
		self.length = 0

		# The string itself.
		self.value = Array(self.context)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.length = 0
		self.value = Array(self.context)

	def read(self, stream):
		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.value = stream.read_chars((self.length))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.length)
		stream.write_chars(self.value)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'SizedString [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* length = {self.length.__repr__()}'
		s += f'\n	* value = {self.value.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
