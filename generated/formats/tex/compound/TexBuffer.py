from source.formats.base.basic import fmt_member
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
		instance.unkn = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint64(instance.offset)
		stream.write_uint64(instance.size)
		stream.write_uint64(instance.unkn)

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
		return f'TexBuffer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* size = {fmt_member(self.size, indent+1)}'
		s += f'\n	* unkn = {fmt_member(self.unkn, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
