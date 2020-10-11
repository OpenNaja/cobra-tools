class UshortVector2:

	"""
	A vector in 2D space (x,y).
	"""

	# First coordinate.
	u: int

	# Second coordinate.
	v: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.u = 0
		self.v = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.u = stream.read_ushort()
		self.v = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushort(self.u)
		stream.write_ushort(self.v)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'UshortVector2 [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* u = ' + self.u.__repr__()
		s += '\n	* v = ' + self.v.__repr__()
		s += '\n'
		return s
