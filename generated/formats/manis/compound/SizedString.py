import typing
from generated.array import Array


class SizedString:

	"""
	A string of given length.
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# The string length.
		self.length = 0

		# The string itself.
		self.value = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.value.read(stream, 'Char', self.length, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.length)
		self.value.write(stream, 'Char', self.length, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'SizedString [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* value = ' + self.value.__repr__()
		s += '\n'
		return s
