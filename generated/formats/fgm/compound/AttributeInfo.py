from source.formats.base.basic import fmt_member
from generated.context import ContextReference


class AttributeInfo:

	"""
	part of fgm fragment, repeated per attribute
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# byte offset to name in fgm buffer
		self.offset = 0

		# 6=bool 5=integer 0=float
		self.dtype = 0

		# byte offset to first value in the 4th fragment entry
		self.value_offset = 0
		self.zero = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.offset = 0
		self.dtype = 0
		self.value_offset = 0
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
		instance.offset = stream.read_uint()
		instance.dtype = stream.read_uint()
		instance.value_offset = stream.read_uint()
		instance.zero = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_uint(instance.offset)
		stream.write_uint(instance.dtype)
		stream.write_uint(instance.value_offset)
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
		return f'AttributeInfo [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* dtype = {fmt_member(self.dtype, indent+1)}'
		s += f'\n	* value_offset = {fmt_member(self.value_offset, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
