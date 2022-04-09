from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class BufferInfoZT:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# in bytes
		self.vertex_buffer_size = 0
		self.zero_0 = 0

		# from start of tris buffer
		self.tris_buffer_size = 0
		self.zero_1 = 0
		self.zero_2 = 0

		# from start of tris buffer
		self.uv_buffer_size = 0
		self.zero_3 = 0
		self.zero_4 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.vertex_buffer_size = 0
		self.zero_0 = 0
		self.tris_buffer_size = 0
		self.zero_1 = 0
		self.zero_2 = 0
		self.uv_buffer_size = 0
		self.zero_3 = 0
		self.zero_4 = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.vertex_buffer_size = stream.read_uint64()
		instance.zero_0 = stream.read_uint64()
		instance.tris_buffer_size = stream.read_uint64()
		instance.zero_1 = stream.read_uint64()
		instance.zero_2 = stream.read_uint64()
		instance.uv_buffer_size = stream.read_uint64()
		instance.zero_3 = stream.read_uint64()
		instance.zero_4 = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64(instance.vertex_buffer_size)
		stream.write_uint64(instance.zero_0)
		stream.write_uint64(instance.tris_buffer_size)
		stream.write_uint64(instance.zero_1)
		stream.write_uint64(instance.zero_2)
		stream.write_uint64(instance.uv_buffer_size)
		stream.write_uint64(instance.zero_3)
		stream.write_uint64(instance.zero_4)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'BufferInfoZT [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* vertex_buffer_size = {fmt_member(self.vertex_buffer_size, indent+1)}'
		s += f'\n	* zero_0 = {fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* tris_buffer_size = {fmt_member(self.tris_buffer_size, indent+1)}'
		s += f'\n	* zero_1 = {fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* zero_2 = {fmt_member(self.zero_2, indent+1)}'
		s += f'\n	* uv_buffer_size = {fmt_member(self.uv_buffer_size, indent+1)}'
		s += f'\n	* zero_3 = {fmt_member(self.zero_3, indent+1)}'
		s += f'\n	* zero_4 = {fmt_member(self.zero_4, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
