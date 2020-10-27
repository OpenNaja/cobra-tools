class Vector4:

	"""
	A vector in 3D space (x,y,z).
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# First coordinate.
		self.x = 0

		# Second coordinate.
		self.y = 0

		# Third coordinate.
		self.z = 0

		# zeroth coordinate.
		self.w = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.x = stream.read_float()
		self.y = stream.read_float()
		self.z = stream.read_float()
		self.w = stream.read_float()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_float(self.x)
		stream.write_float(self.y)
		stream.write_float(self.z)
		stream.write_float(self.w)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		return "[ %6.3f %6.3f %6.3f %6.3f ]"%(self.x, self.y, self.z, self.w)

