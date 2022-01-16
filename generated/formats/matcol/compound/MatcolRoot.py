from generated.context import ContextReference


class MatcolRoot:

	"""
	ss data
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# root ptr
		self.ptr = 0

		# always 1
		self.one = 0
		self.set_defaults()

	def set_defaults(self):
		self.ptr = 0
		self.one = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.ptr = stream.read_uint64()
		self.one = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.ptr)
		stream.write_uint64(self.one)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'MatcolRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* ptr = {self.ptr.__repr__()}'
		s += f'\n	* one = {self.one.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
