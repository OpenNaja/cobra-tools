from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class BufferGroup:

	"""
	32 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# first buffer index
		self.buffer_offset = 0

		# number of buffers to grab
		self.buffer_count = 0

		# type of extension this entry is for
		self.ext_index = 0

		# which buffer index to populate
		self.buffer_index = 0

		# cumulative size of all buffers to grab
		self.size = 0

		# first data entry
		self.data_offset = 0

		# number of data entries to populate buffers into
		self.data_count = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.buffer_offset = 0
		self.buffer_count = 0
		self.ext_index = 0
		self.buffer_index = 0
		self.size = 0
		self.data_offset = 0
		self.data_count = 0

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
		instance.buffer_offset = stream.read_uint()
		instance.buffer_count = stream.read_uint()
		instance.ext_index = stream.read_uint()
		instance.buffer_index = stream.read_uint()
		instance.size = stream.read_uint64()
		instance.data_offset = stream.read_uint()
		instance.data_count = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.buffer_offset)
		stream.write_uint(instance.buffer_count)
		stream.write_uint(instance.ext_index)
		stream.write_uint(instance.buffer_index)
		stream.write_uint64(instance.size)
		stream.write_uint(instance.data_offset)
		stream.write_uint(instance.data_count)

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
		return f'BufferGroup [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* buffer_offset = {fmt_member(self.buffer_offset, indent+1)}'
		s += f'\n	* buffer_count = {fmt_member(self.buffer_count, indent+1)}'
		s += f'\n	* ext_index = {fmt_member(self.ext_index, indent+1)}'
		s += f'\n	* buffer_index = {fmt_member(self.buffer_index, indent+1)}'
		s += f'\n	* size = {fmt_member(self.size, indent+1)}'
		s += f'\n	* data_offset = {fmt_member(self.data_offset, indent+1)}'
		s += f'\n	* data_count = {fmt_member(self.data_count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
