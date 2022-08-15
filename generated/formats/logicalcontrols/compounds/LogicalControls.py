import generated.formats.base.basic
import generated.formats.logicalcontrols.compounds.AxisValue
import generated.formats.logicalcontrols.compounds.Button
import generated.formats.logicalcontrols.compounds.Some
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class LogicalControls(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.button_count = 0
		self.axis_count = 0
		self.count_3 = 0
		self.count_4 = 0
		self.flags = 0
		self.buttons = ArrayPointer(self.context, self.button_count, generated.formats.logicalcontrols.compounds.Button.Button)
		self.axes = ArrayPointer(self.context, self.axis_count, generated.formats.logicalcontrols.compounds.AxisValue.AxisValue)
		self.c = ArrayPointer(self.context, self.count_3, )
		self.d = ArrayPointer(self.context, self.count_4, generated.formats.logicalcontrols.compounds.Some.Some)
		self.unsure = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.button_count = 0
		self.axis_count = 0
		self.count_3 = 0
		self.count_4 = 0
		self.flags = 0
		self.buttons = ArrayPointer(self.context, self.button_count, generated.formats.logicalcontrols.compounds.Button.Button)
		self.axes = ArrayPointer(self.context, self.axis_count, generated.formats.logicalcontrols.compounds.AxisValue.AxisValue)
		self.c = ArrayPointer(self.context, self.count_3, )
		self.d = ArrayPointer(self.context, self.count_4, generated.formats.logicalcontrols.compounds.Some.Some)
		self.unsure = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.buttons = ArrayPointer.from_stream(stream, instance.context, instance.button_count, generated.formats.logicalcontrols.compounds.Button.Button)
		instance.axes = ArrayPointer.from_stream(stream, instance.context, instance.axis_count, generated.formats.logicalcontrols.compounds.AxisValue.AxisValue)
		instance.c = ArrayPointer.from_stream(stream, instance.context, instance.count_3, )
		instance.d = ArrayPointer.from_stream(stream, instance.context, instance.count_4, generated.formats.logicalcontrols.compounds.Some.Some)
		instance.button_count = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.axis_count = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_3 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_4 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.flags = Uint.from_stream(stream, instance.context, 0, None)
		instance.unsure = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		if not isinstance(instance.buttons, int):
			instance.buttons.arg = instance.button_count
		if not isinstance(instance.axes, int):
			instance.axes.arg = instance.axis_count
		if not isinstance(instance.c, int):
			instance.c.arg = instance.count_3
		if not isinstance(instance.d, int):
			instance.d.arg = instance.count_4
		if not isinstance(instance.unsure, int):
			instance.unsure.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.buttons)
		ArrayPointer.to_stream(stream, instance.axes)
		ArrayPointer.to_stream(stream, instance.c)
		ArrayPointer.to_stream(stream, instance.d)
		stream.write_ubyte(instance.button_count)
		stream.write_ubyte(instance.axis_count)
		stream.write_ubyte(instance.count_3)
		stream.write_ubyte(instance.count_4)
		stream.write_uint(instance.flags)
		Pointer.to_stream(stream, instance.unsure)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'buttons', ArrayPointer, (instance.button_count, generated.formats.logicalcontrols.compounds.Button.Button)
		yield 'axes', ArrayPointer, (instance.axis_count, generated.formats.logicalcontrols.compounds.AxisValue.AxisValue)
		yield 'c', ArrayPointer, (instance.count_3, )
		yield 'd', ArrayPointer, (instance.count_4, generated.formats.logicalcontrols.compounds.Some.Some)
		yield 'button_count', Ubyte, (0, None)
		yield 'axis_count', Ubyte, (0, None)
		yield 'count_3', Ubyte, (0, None)
		yield 'count_4', Ubyte, (0, None)
		yield 'flags', Uint, (0, None)
		yield 'unsure', Pointer, (0, generated.formats.base.basic.ZString)

	def get_info_str(self, indent=0):
		return f'LogicalControls [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* buttons = {self.fmt_member(self.buttons, indent+1)}'
		s += f'\n	* axes = {self.fmt_member(self.axes, indent+1)}'
		s += f'\n	* c = {self.fmt_member(self.c, indent+1)}'
		s += f'\n	* d = {self.fmt_member(self.d, indent+1)}'
		s += f'\n	* button_count = {self.fmt_member(self.button_count, indent+1)}'
		s += f'\n	* axis_count = {self.fmt_member(self.axis_count, indent+1)}'
		s += f'\n	* count_3 = {self.fmt_member(self.count_3, indent+1)}'
		s += f'\n	* count_4 = {self.fmt_member(self.count_4, indent+1)}'
		s += f'\n	* flags = {self.fmt_member(self.flags, indent+1)}'
		s += f'\n	* unsure = {self.fmt_member(self.unsure, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
