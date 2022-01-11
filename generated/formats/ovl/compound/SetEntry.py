from generated.context import ContextReference


class SetEntry:

	"""
	the asset indices of two consecutive SetEntries define a set of AssetEntries
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.file_hash = 0
		self.ext_hash = 0

		# add from last set's entry up to this index to this set
		self.start = 0
		self.set_defaults()

	def set_defaults(self):
		self.file_hash = 0
		if self.context.version >= 19:
			self.ext_hash = 0
		self.start = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.file_hash = stream.read_uint()
		if self.context.version >= 19:
			self.ext_hash = stream.read_uint()
		self.start = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.file_hash)
		if self.context.version >= 19:
			stream.write_uint(self.ext_hash)
		stream.write_uint(self.start)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'SetEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* file_hash = {self.file_hash.__repr__()}'
		s += f'\n	* ext_hash = {self.ext_hash.__repr__()}'
		s += f'\n	* start = {self.start.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
