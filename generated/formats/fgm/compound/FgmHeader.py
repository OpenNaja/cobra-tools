from generated.context import ContextReference


class FgmHeader:

	"""
	Sized str entry of 16 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Number of Texture Info Entries
		self.texture_count = 0

		# Number of Attribute Info Entries
		self.attribute_count = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.texture_count = 0
		self.attribute_count = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.texture_count = stream.read_uint64()
		self.attribute_count = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.texture_count)
		stream.write_uint64(self.attribute_count)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'FgmHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* texture_count = {self.texture_count.__repr__()}'
		s += f'\n	* attribute_count = {self.attribute_count.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
