from source.formats.base.basic import fmt_member
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.StreamInfo import StreamInfo


class BufferInfoZT:

	"""
	from here on, it's buffer 1
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.streams = Array((self.arg,), StreamInfo, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.streams = Array((self.arg,), StreamInfo, self.context, 0, None)

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
		instance.streams = Array.from_stream(stream, (instance.arg,), StreamInfo, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		Array.to_stream(stream, instance.streams, (instance.arg,), StreamInfo, instance.context, 0, None)

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
		s += f'\n	* streams = {fmt_member(self.streams, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
