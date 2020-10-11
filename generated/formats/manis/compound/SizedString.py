import typing


class SizedString:

	"""
	A string of given length.
	"""

	# The string length.
	length: int

	# The string itself.
	value: typing.List[Char]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.length = 0
		self.value = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.value = [stream.read_char() for _ in range(self.length)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.length)
		for item in self.value: stream.write_char(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'SizedString [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* value = ' + self.value.__repr__()
		s += '\n'
		return s
