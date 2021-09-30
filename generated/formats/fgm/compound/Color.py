from generated.context import ContextReference


class Color:

	"""
	4 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.r = 0
		self.g = 0
		self.b = 0
		self.a = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.r = stream.read_ubyte()
		self.g = stream.read_ubyte()
		self.b = stream.read_ubyte()
		self.a = stream.read_ubyte()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ubyte(self.r)
		stream.write_ubyte(self.g)
		stream.write_ubyte(self.b)
		stream.write_ubyte(self.a)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Color [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* r = {self.r.__repr__()}'
		s += f'\n	* g = {self.g.__repr__()}'
		s += f'\n	* b = {self.b.__repr__()}'
		s += f'\n	* a = {self.a.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
