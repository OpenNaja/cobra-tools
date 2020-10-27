class Vector3Ushort:

	"""
	A signed int16 vector in 3D space (x,y,z).
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

	def read(self, stream):

		self.io_start = stream.tell()
		self.x = stream.read_ushort()
		self.y = stream.read_ushort()
		self.z = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushort(self.x)
		stream.write_ushort(self.y)
		stream.write_ushort(self.z)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'Vector3Ushort [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* x = ' + self.x.__repr__()
		s += '\n	* y = ' + self.y.__repr__()
		s += '\n	* z = ' + self.z.__repr__()
		s += '\n'
		return s
