import generated.formats.base.basic
import generated.formats.logicalcontrols.compounds.ButtonData
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Button(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.datas_count = 0
		self.flags = 0
		self.button_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.datas = ArrayPointer(self.context, self.datas_count, generated.formats.logicalcontrols.compounds.ButtonData.ButtonData)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.datas_count = 0
		self.flags = 0
		self.button_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.datas = ArrayPointer(self.context, self.datas_count, generated.formats.logicalcontrols.compounds.ButtonData.ButtonData)

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
		instance.button_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.datas = ArrayPointer.from_stream(stream, instance.context, instance.datas_count, generated.formats.logicalcontrols.compounds.ButtonData.ButtonData)
		instance.datas_count = stream.read_uint()
		instance.flags = stream.read_uint()
		if not isinstance(instance.button_name, int):
			instance.button_name.arg = 0
		if not isinstance(instance.datas, int):
			instance.datas.arg = instance.datas_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.button_name)
		ArrayPointer.to_stream(stream, instance.datas)
		stream.write_uint(instance.datas_count)
		stream.write_uint(instance.flags)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'button_name', Pointer, (0, generated.formats.base.basic.ZString)
		yield 'datas', ArrayPointer, (instance.datas_count, generated.formats.logicalcontrols.compounds.ButtonData.ButtonData)
		yield 'datas_count', Uint, (0, None)
		yield 'flags', Uint, (0, None)

	def get_info_str(self, indent=0):
		return f'Button [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* button_name = {self.fmt_member(self.button_name, indent+1)}'
		s += f'\n	* datas = {self.fmt_member(self.datas, indent+1)}'
		s += f'\n	* datas_count = {self.fmt_member(self.datas_count, indent+1)}'
		s += f'\n	* flags = {self.fmt_member(self.flags, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
