from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class OffsetChunk:

	"""
	used in JWE2 Biosyn
	16 bytes
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.flag = 0

		# scale: pack_offset / 512, also added as offset
		self.pack_offset = 0.0

		# byte offset from start of vert buffer in bytes
		self.vertex_offset = 0
		self.vertex_count = 0

		# unsure
		self.some_count = 0
		self.zero = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.flag = 0
		self.pack_offset = 0.0
		self.vertex_offset = 0
		self.vertex_count = 0
		self.some_count = 0
		self.zero = 0

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
		instance.flag = stream.read_uint()
		instance.pack_offset = stream.read_float()
		instance.vertex_offset = stream.read_uint()
		instance.vertex_count = stream.read_ubyte()
		instance.some_count = stream.read_ushort()
		instance.zero = stream.read_ubyte()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.flag)
		stream.write_float(instance.pack_offset)
		stream.write_uint(instance.vertex_offset)
		stream.write_ubyte(instance.vertex_count)
		stream.write_ushort(instance.some_count)
		stream.write_ubyte(instance.zero)

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
		return f'OffsetChunk [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* flag = {fmt_member(self.flag, indent+1)}'
		s += f'\n	* pack_offset = {fmt_member(self.pack_offset, indent+1)}'
		s += f'\n	* vertex_offset = {fmt_member(self.vertex_offset, indent+1)}'
		s += f'\n	* vertex_count = {fmt_member(self.vertex_count, indent+1)}'
		s += f'\n	* some_count = {fmt_member(self.some_count, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
