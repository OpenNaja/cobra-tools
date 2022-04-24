from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class StreamInfo:

	"""
	Describes a wem file in an s type bank stream
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.offset = 0
		self.size = 0

		# referred to by the events aux file
		self.event_id = 0
		self.zero = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.offset = 0
		self.size = 0
		self.event_id = 0
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
		instance.offset = stream.read_uint64()
		instance.size = stream.read_uint64()
		instance.event_id = stream.read_uint()
		instance.zero = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64(instance.offset)
		stream.write_uint64(instance.size)
		stream.write_uint(instance.event_id)
		stream.write_uint(instance.zero)

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
		return f'StreamInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* size = {fmt_member(self.size, indent+1)}'
		s += f'\n	* event_id = {fmt_member(self.event_id, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
