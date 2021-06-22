class UshortVector2:

	"""
	A vector in 2D space (x,y).
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# First coordinate.
		self.u = 0

		# Second coordinate.
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

	def get_info_str(self):
		return f'UshortVector2 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* u = {self.u.__repr__()}'
		s += f'\n	* v = {self.v.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
