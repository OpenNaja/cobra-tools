from source.formats.base.basic import fmt_member
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.InfoZTMemPool import InfoZTMemPool
from generated.formats.ovl_base.compound.SmartPadding import SmartPadding


class BufferInfoZTHeader:

	"""
	Data describing a MS2 buffer giving the size of the whole vertex and tri buffer.
	266 bytes
	very end of buffer 0 after the names list
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# sometimes 00 byte
		self.weird_padding = SmartPadding(self.context, 0, None)

		# ?
		self.unks = Array((self.arg.unk_count,), InfoZTMemPool, self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.weird_padding = SmartPadding(self.context, 0, None)
		self.unks = Array((self.arg.unk_count,), InfoZTMemPool, self.context, 0, None)

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
		instance.weird_padding = SmartPadding.from_stream(stream, instance.context, 0, None)
		instance.unks = Array.from_stream(stream, (instance.arg.unk_count,), InfoZTMemPool, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		SmartPadding.to_stream(stream, instance.weird_padding)
		Array.to_stream(stream, instance.unks, (instance.arg.unk_count,), InfoZTMemPool, instance.context, 0, None)

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
		return f'BufferInfoZTHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* weird_padding = {fmt_member(self.weird_padding, indent+1)}'
		s += f'\n	* unks = {fmt_member(self.unks, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
