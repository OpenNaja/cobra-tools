import typing


class ManisSizedStrData:

# per attribute

	# 96 in driver
	unknown_0: int

	# 272 in driver
	unknown_1: int

	# zeros in driver
	unknown_2: typing.List[int]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.unknown_0 = stream.read_ushort()
		self.unknown_1 = stream.read_ushort()
		self.unknown_2 = [stream.read_uint() for _ in range(5)]

	def write(self, stream):
		stream.write_ushort(self.unknown_0)
		stream.write_ushort(self.unknown_1)
		for item in self.unknown_2: stream.write_uint(item)

	def __repr__(self):
		s = 'ManisSizedStrData'
		s += '\nunknown_0 ' + self.unknown_0.__repr__()
		s += '\nunknown_1 ' + self.unknown_1.__repr__()
		s += '\nunknown_2 ' + self.unknown_2.__repr__()
		s += '\n'
		return s