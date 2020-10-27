class HeaderType:

	"""
	Located at start of deflated archive stream
	"""

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Type of the headers that follow
		self.type = 0

		# Amount of the headers of that type that follow the headers block
		self.num_headers = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.type = stream.read_ushort()
		self.num_headers = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushort(self.type)
		stream.write_ushort(self.num_headers)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'HeaderType [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* type = ' + self.type.__repr__()
		s += '\n	* num_headers = ' + self.num_headers.__repr__()
		s += '\n'
		return s
