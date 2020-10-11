import typing


class TypeOther:

	"""
	generic
	"""

	# length of this section
	length: int

	# id of this Sound SFX object
	raw: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.length = 0
		self.raw = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.length = stream.read_uint()
		self.raw = [stream.read_byte() for _ in range(self.length)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.length)
		for item in self.raw: stream.write_byte(item)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'TypeOther [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* raw = ' + self.raw.__repr__()
		s += '\n'
		return s
