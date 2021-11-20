from generated.context import ContextReference


class TexBuffer:

	"""
	Part of a fragment, repeated for count of texture LODs / buffers.
	Data struct for headers of type 3
	24 bytes per texture buffer
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# byte offset in the combined buffer
		self.offset = 0

		# byte size of this tex buffer
		self.size = 0

		# is also related to data size
		self.unkn = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.offset = 0
		self.size = 0
		self.unkn = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.offset = stream.read_uint64()
		self.size = stream.read_uint64()
		self.unkn = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.offset)
		stream.write_uint64(self.size)
		stream.write_uint64(self.unkn)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'TexBuffer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* offset = {self.offset.__repr__()}'
		s += f'\n	* size = {self.size.__repr__()}'
		s += f'\n	* unkn = {self.unkn.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
