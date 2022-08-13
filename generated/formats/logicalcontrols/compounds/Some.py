import generated.formats.base.basic
import generated.formats.logicalcontrols.compounds.SomeData
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Some(MemStruct):

	"""
	24 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.some_count = 0
		self.some_name = 0
		self.some_data = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.some_count = 0
		self.some_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.some_data = ArrayPointer(self.context, self.some_count, generated.formats.logicalcontrols.compounds.SomeData.SomeData)

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
		instance.some_data = ArrayPointer.from_stream(stream, instance.context, instance.some_count, generated.formats.logicalcontrols.compounds.SomeData.SomeData)
		instance.some_count = stream.read_uint64()
		if not isinstance(instance.some_name, int):
			instance.some_name.arg = 0
		if not isinstance(instance.some_data, int):
			instance.some_data.arg = instance.some_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.some_name)
		ArrayPointer.to_stream(stream, instance.some_data)
		stream.write_uint64(instance.some_count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('some_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('some_data', ArrayPointer, (instance.some_count, generated.formats.logicalcontrols.compounds.SomeData.SomeData))
		yield ('some_count', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'Some [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* some_name = {self.fmt_member(self.some_name, indent+1)}'
		s += f'\n	* some_data = {self.fmt_member(self.some_data, indent+1)}'
		s += f'\n	* some_count = {self.fmt_member(self.some_count, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
