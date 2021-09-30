from generated.context import ContextReference


class Vector3Short:

	"""
	A signed int16 vector in 3D space (x,y,z).
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

	def read(self, stream):

		self.io_start = stream.tell()
		self.x = stream.read_short()
		self.y = stream.read_short()
		self.z = stream.read_short()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_short(self.x)
		stream.write_short(self.y)
		stream.write_short(self.z)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Vector3Short [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

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
