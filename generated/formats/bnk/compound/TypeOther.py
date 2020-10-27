import typing
from generated.array import Array


class TypeOther:

	"""
	generic
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# length of this section
		self.length = 0

		# id of this Sound SFX object
		self.raw = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.raw.read(stream, 'Byte', self.length, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.length)
		self.raw.write(stream, 'Byte', self.length, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'TypeOther [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* raw = ' + self.raw.__repr__()
		s += '\n'
		return s
