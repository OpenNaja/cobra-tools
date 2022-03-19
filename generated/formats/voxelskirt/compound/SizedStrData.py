from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class SizedStrData:

	"""
	# size varies according to game
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zero = 0

		# total size of buffer data
		self.data_size = 0
		self.x = 0
		self.y = 0
		self.scale = 0.0
		self.padding = 0.0

		# zero, for PC only
		self.zero_pc = 0

		# x*y*4, for PC only
		self.height_array_size_pc = 0
		self.data_offset = 0

		# entries of 32 bytes
		self.data_count = 0
		self.size_offset = 0

		# entries of 40 bytes
		self.size_count = 0

		# slightly smaller than total size of buffer data
		self.position_offset = 0

		# counts the -1 structs; entries of 32 bytes
		self.position_count = 0

		# offset into buffer to start of sth; only given if some count is nonzero
		self.mat_offset = 0
		self.mat_count = 0

		# offset into buffer to start of name zstrings
		self.name_buffer_offset = 0

		# also counts the stuff after names
		self.name_count = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.zero = 0
		self.data_size = 0
		self.x = 0
		self.y = 0
		self.scale = 0.0
		self.padding = 0.0
		if self.context.version == 18:
			self.zero_pc = 0
		if self.context.version == 18:
			self.height_array_size_pc = 0
		if not (self.context.version == 18):
			self.data_offset = 0
		if not (self.context.version == 18):
			self.data_count = 0
		if not (self.context.version == 18):
			self.size_offset = 0
		if not (self.context.version == 18):
			self.size_count = 0
		self.position_offset = 0
		self.position_count = 0
		self.mat_offset = 0
		self.mat_count = 0
		self.name_buffer_offset = 0
		self.name_count = 0

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
		instance.zero = stream.read_uint64()
		instance.data_size = stream.read_uint64()
		instance.x = stream.read_uint64()
		instance.y = stream.read_uint64()
		instance.scale = stream.read_float()
		instance.padding = stream.read_float()
		if instance.context.version == 18:
			instance.zero_pc = stream.read_uint64()
			instance.height_array_size_pc = stream.read_uint64()
		if not (instance.context.version == 18):
			instance.data_offset = stream.read_uint64()
			instance.data_count = stream.read_uint64()
		if not (instance.context.version == 18):
			instance.size_offset = stream.read_uint64()
			instance.size_count = stream.read_uint64()
		instance.position_offset = stream.read_uint64()
		instance.position_count = stream.read_uint64()
		instance.mat_offset = stream.read_uint64()
		instance.mat_count = stream.read_uint64()
		instance.name_buffer_offset = stream.read_uint64()
		instance.name_count = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64(instance.zero)
		stream.write_uint64(instance.data_size)
		stream.write_uint64(instance.x)
		stream.write_uint64(instance.y)
		stream.write_float(instance.scale)
		stream.write_float(instance.padding)
		if instance.context.version == 18:
			stream.write_uint64(instance.zero_pc)
			stream.write_uint64(instance.height_array_size_pc)
		if not (instance.context.version == 18):
			stream.write_uint64(instance.data_offset)
			stream.write_uint64(instance.data_count)
		if not (instance.context.version == 18):
			stream.write_uint64(instance.size_offset)
			stream.write_uint64(instance.size_count)
		stream.write_uint64(instance.position_offset)
		stream.write_uint64(instance.position_count)
		stream.write_uint64(instance.mat_offset)
		stream.write_uint64(instance.mat_count)
		stream.write_uint64(instance.name_buffer_offset)
		stream.write_uint64(instance.name_count)

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
		return f'SizedStrData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		s += f'\n	* data_size = {fmt_member(self.data_size, indent+1)}'
		s += f'\n	* x = {fmt_member(self.x, indent+1)}'
		s += f'\n	* y = {fmt_member(self.y, indent+1)}'
		s += f'\n	* scale = {fmt_member(self.scale, indent+1)}'
		s += f'\n	* padding = {fmt_member(self.padding, indent+1)}'
		s += f'\n	* zero_pc = {fmt_member(self.zero_pc, indent+1)}'
		s += f'\n	* height_array_size_pc = {fmt_member(self.height_array_size_pc, indent+1)}'
		s += f'\n	* data_offset = {fmt_member(self.data_offset, indent+1)}'
		s += f'\n	* data_count = {fmt_member(self.data_count, indent+1)}'
		s += f'\n	* size_offset = {fmt_member(self.size_offset, indent+1)}'
		s += f'\n	* size_count = {fmt_member(self.size_count, indent+1)}'
		s += f'\n	* position_offset = {fmt_member(self.position_offset, indent+1)}'
		s += f'\n	* position_count = {fmt_member(self.position_count, indent+1)}'
		s += f'\n	* mat_offset = {fmt_member(self.mat_offset, indent+1)}'
		s += f'\n	* mat_count = {fmt_member(self.mat_count, indent+1)}'
		s += f'\n	* name_buffer_offset = {fmt_member(self.name_buffer_offset, indent+1)}'
		s += f'\n	* name_count = {fmt_member(self.name_count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
