class UnknownEntry:

# Description of one file type
	unknown_1: int
	unknown_2: int
	unknown_3: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.unknown_1 = stream.read_uint()
		self.unknown_2 = stream.read_uint()
		self.unknown_3 = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.unknown_1)
		stream.write_uint(self.unknown_2)
		stream.write_uint(self.unknown_3)

	def __repr__(self):
		s = 'UnknownEntry'
		s += '\nunknown_1 ' + self.unknown_1.__repr__()
		s += '\nunknown_2 ' + self.unknown_2.__repr__()
		s += '\nunknown_3 ' + self.unknown_3.__repr__()
		s += '\n'
		return s