from generated.context import ContextReference


class UbyteVector3:

	"""
	A vector in 3D space (x,y,z).
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
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
		self.set_defaults()

	def set_defaults(self):
		self.x = 0
		self.y = 0
		self.z = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.x = stream.read_ubyte()
		self.y = stream.read_ubyte()
		self.z = stream.read_ubyte()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_ubyte(self.x)
		stream.write_ubyte(self.y)
		stream.write_ubyte(self.z)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'UbyteVector3 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* x = {self.x.__repr__()}'
		s += f'\n	* y = {self.y.__repr__()}'
		s += f'\n	* z = {self.z.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
