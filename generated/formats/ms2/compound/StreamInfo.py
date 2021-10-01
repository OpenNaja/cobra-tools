from generated.context import ContextReference


class StreamInfo:

	"""
	Fragment data describing a MS2 buffer giving the size of the whole vertex and tri buffer.
	64 bytes
	this has the starting offsets of tri buffers per streamed buffer
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# in bytes
		self.vertex_buffer_length = 0
		self.zero_0 = 0

		# from start of tris buffer
		self.tris_buffer_length = 0
		self.zero_1 = 0
		self.zero_2 = 0

		# from start of tris buffer
		self.uv_buffer_length = 0
		self.zero_3 = 0
		self.zero_4 = 0
		self.set_defaults()

	def set_defaults(self):
		self.vertex_buffer_length = 0
		self.zero_0 = 0
		self.tris_buffer_length = 0
		self.zero_1 = 0
		self.zero_2 = 0
		self.uv_buffer_length = 0
		self.zero_3 = 0
		self.zero_4 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.vertex_buffer_length = stream.read_uint64()
		self.zero_0 = stream.read_uint64()
		self.tris_buffer_length = stream.read_uint64()
		self.zero_1 = stream.read_uint64()
		self.zero_2 = stream.read_uint64()
		self.uv_buffer_length = stream.read_uint64()
		self.zero_3 = stream.read_uint64()
		self.zero_4 = stream.read_uint64()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_uint64(self.vertex_buffer_length)
		stream.write_uint64(self.zero_0)
		stream.write_uint64(self.tris_buffer_length)
		stream.write_uint64(self.zero_1)
		stream.write_uint64(self.zero_2)
		stream.write_uint64(self.uv_buffer_length)
		stream.write_uint64(self.zero_3)
		stream.write_uint64(self.zero_4)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'StreamInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* vertex_buffer_length = {self.vertex_buffer_length.__repr__()}'
		s += f'\n	* zero_0 = {self.zero_0.__repr__()}'
		s += f'\n	* tris_buffer_length = {self.tris_buffer_length.__repr__()}'
		s += f'\n	* zero_1 = {self.zero_1.__repr__()}'
		s += f'\n	* zero_2 = {self.zero_2.__repr__()}'
		s += f'\n	* uv_buffer_length = {self.uv_buffer_length.__repr__()}'
		s += f'\n	* zero_3 = {self.zero_3.__repr__()}'
		s += f'\n	* zero_4 = {self.zero_4.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
