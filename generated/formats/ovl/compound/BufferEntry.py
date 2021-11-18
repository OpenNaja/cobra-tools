from generated.context import ContextReference


class BufferEntry:

	"""
	8 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index of buffer in file, up to pz 1.6
		self.index = 0

		# in bytes
		self.size = 0

		# id, new for pz 1.6
		self.file_hash = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.context.version <= 19:
			self.index = 0
		self.size = 0
		if self.context.version >= 20:
			self.file_hash = 0

	def read(self, stream):
		self.io_start = stream.tell()
		if self.context.version <= 19:
			self.index = stream.read_uint()
		self.size = stream.read_uint()
		if self.context.version >= 20:
			self.file_hash = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		if self.context.version <= 19:
			stream.write_uint(self.index)
		stream.write_uint(self.size)
		if self.context.version >= 20:
			stream.write_uint(self.file_hash)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'BufferEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* index = {self.index.__repr__()}'
		s += f'\n	* size = {self.size.__repr__()}'
		s += f'\n	* file_hash = {self.file_hash.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s

	def read_data(self, stream):
		"""Load data from archive stream into self for modification and io"""
		self.data = stream.read(self.size)

	def update_data(self, data):
		"""Set data internal data so it can be written on save and update the size value"""
		self.data = data
		self.size = len(data)
