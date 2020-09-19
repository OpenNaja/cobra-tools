class OtherEntry:

# ?
	unknown_00: int
	unknown_08: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.unknown_00 = stream.read_uint()
		self.unknown_08 = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.unknown_00)
		stream.write_uint(self.unknown_08)

	def __repr__(self):
		s = 'OtherEntry'
		s += '\nunknown_00 ' + self.unknown_00.__repr__()
		s += '\nunknown_08 ' + self.unknown_08.__repr__()
		s += '\n'
		return s