class Vector4:

	"""
	A vector in 3D space (x,y,z).
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# zeroth coordinate.
		self.w = 0

		# First coordinate.
		self.x = 0

		# Second coordinate.
		self.y = 0

		# Third coordinate.
		self.z = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.w = stream.read_float()
		self.x = stream.read_float()
		self.y = stream.read_float()
		self.z = stream.read_float()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_float(self.w)
		stream.write_float(self.x)
		stream.write_float(self.y)
		stream.write_float(self.z)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Vector4 [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* w = ' + self.w.__repr__()
		s += '\n	* x = ' + self.x.__repr__()
		s += '\n	* y = ' + self.y.__repr__()
		s += '\n	* z = ' + self.z.__repr__()
		s += '\n'
		return s
