from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.logicalcontrols.compound.SomeData
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class Some(MemStruct):

	"""
	24 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.some_count = 0
		self.some_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.some_data = ArrayPointer(self.context, self.some_count, generated.formats.logicalcontrols.compound.SomeData.SomeData)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.some_count = 0
		self.some_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.some_data = ArrayPointer(self.context, self.some_count, generated.formats.logicalcontrols.compound.SomeData.SomeData)

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
		instance.some_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.some_data = ArrayPointer.from_stream(stream, instance.context, instance.some_count, generated.formats.logicalcontrols.compound.SomeData.SomeData)
		instance.some_count = stream.read_uint64()
		instance.some_name.arg = 0
		instance.some_data.arg = instance.some_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.some_name)
		ArrayPointer.to_stream(stream, instance.some_data)
		stream.write_uint64(instance.some_count)

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
		return f'Some [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* some_name = {fmt_member(self.some_name, indent+1)}'
		s += f'\n	* some_data = {fmt_member(self.some_data, indent+1)}'
		s += f'\n	* some_count = {fmt_member(self.some_count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
