from source.formats.base.basic import fmt_member
import generated.formats.specdef.compound.Data
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer
from generated.formats.specdef.enum.SpecdefDtype import SpecdefDtype


class ArrayData(MemStruct):

	"""
	16 bytes in log
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default=False)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.dtype = SpecdefDtype(self.context, 0, None)
		self.unused = 0
		self.item = Pointer(self.context, self.dtype, generated.formats.specdef.compound.Data.Data)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.dtype = SpecdefDtype(self.context, 0, None)
		self.unused = 0
		self.item = Pointer(self.context, self.dtype, generated.formats.specdef.compound.Data.Data)

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
		instance.item = Pointer.from_stream(stream, instance.context, instance.dtype, generated.formats.specdef.compound.Data.Data)
		instance.dtype = SpecdefDtype.from_value(stream.read_uint())
		instance.unused = stream.read_uint()
		instance.item.arg = instance.dtype

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.item)
		stream.write_uint(instance.dtype.value)
		stream.write_uint(instance.unused)

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
		return f'ArrayData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* item = {fmt_member(self.item, indent+1)}'
		s += f'\n	* dtype = {fmt_member(self.dtype, indent+1)}'
		s += f'\n	* unused = {fmt_member(self.unused, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
