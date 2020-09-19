class MotionGraphVarsStrData:

# per attribute

	# 4 in driver
	unknown_0: int

	# 0 in driver
	unknown_1: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template

	def read(self, stream):
		self.unknown_0 = stream.read_uint()
		self.unknown_1 = stream.read_uint()

	def write(self, stream):
		stream.write_uint(self.unknown_0)
		stream.write_uint(self.unknown_1)

	def __repr__(self):
		s = 'MotionGraphVarsStrData'
		s += '\nunknown_0 ' + self.unknown_0.__repr__()
		s += '\nunknown_1 ' + self.unknown_1.__repr__()
		s += '\n'
		return s