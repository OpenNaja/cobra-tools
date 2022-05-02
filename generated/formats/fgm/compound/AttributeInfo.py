from source.formats.base.basic import fmt_member
from generated.formats.fgm.enum.FgmDtype import FgmDtype
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class AttributeInfo(MemStruct):

	"""
	part of fgm fragment, repeated per attribute
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# byte offset to name in fgm buffer
		self.offset = 0
		self.dtype = FgmDtype(self.context, 0, None)

		# byte offset to first value in the data_lib pointer
		self.value_offset = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.offset = 0
		self.dtype = FgmDtype(self.context, 0, None)
		self.value_offset = 0

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
		super().read_fields(stream, instance)
		instance.offset = stream.read_uint()
		instance.dtype = FgmDtype.from_value(stream.read_uint())
		instance.value_offset = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.offset)
		stream.write_uint(instance.dtype.value)
		stream.write_uint64(instance.value_offset)

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
		s += super().get_fields_str()
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* dtype = {fmt_member(self.dtype, indent+1)}'
		s += f'\n	* value_offset = {fmt_member(self.value_offset, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
