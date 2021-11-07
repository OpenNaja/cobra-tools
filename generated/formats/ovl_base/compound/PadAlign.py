from generated.context import ContextReference


class PadAlign:

	"""
	Grabs 00 bytes only
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.set_defaults()

	def set_defaults(self):
		pass

	def read(self, stream):
		self.io_start = stream.tell()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'PadAlign [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
