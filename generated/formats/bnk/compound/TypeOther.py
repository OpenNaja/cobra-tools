import typing


class TypeOther:

# generic

	# length of this section
	length: int

	# id of this Sound SFX object
	raw: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.length = 0
		self.raw = 0

	def read(self, stream):
		self.length = stream.read_uint()
		self.raw = [stream.read_byte() for _ in range(self.length)]

	def write(self, stream):
		stream.write_uint(self.length)
		for item in self.raw: stream.write_byte(item)

	def __repr__(self):
		s = 'TypeOther'
		s += '\n	* length = ' + self.length.__repr__()
		s += '\n	* raw = ' + self.raw.__repr__()
		s += '\n'
		return s