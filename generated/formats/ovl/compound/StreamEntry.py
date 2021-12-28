from generated.context import ContextReference


class StreamEntry:

	"""
	Description of one streamed file instance. One for every file stored in an ovs.
	Links the main pointers of a streamed file to its user, eg. a texturestream to a tex file.
	--These appear sorted in the order of sizedstr entries per ovs.-- only true for lod0, not lod1
	the order does not seem to be consistent
	interestingly, the order of ss entries per ovs is consistent with decreasing pool offset
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# offset to the stream's ss pointer inside the flattened mempools
		self.stream_offset = 0

		# offset to the user file's ss pointer (in STATIC) inside the flattened mempools
		self.file_offset = 0
		self.zero = 0
		self.set_defaults()

	def set_defaults(self):
		self.stream_offset = 0
		self.file_offset = 0
		self.zero = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.stream_offset = stream.read_uint()
		self.file_offset = stream.read_uint()
		self.zero = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint(self.stream_offset)
		stream.write_uint(self.file_offset)
		stream.write_uint(self.zero)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'StreamEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* stream_offset = {self.stream_offset.__repr__()}'
		s += f'\n	* file_offset = {self.file_offset.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
