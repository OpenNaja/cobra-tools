from generated.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.logicalcontrols.compound.AxisValue
import generated.formats.logicalcontrols.compound.Button
import generated.formats.logicalcontrols.compound.Some
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compound.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class LogicalControls(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.button_count = 0
		self.axis_count = 0
		self.count_3 = 0
		self.count_4 = 0
		self.flags = 0
		self.buttons = 0
		self.axes = 0
		self.c = 0
		self.d = 0
		self.unsure = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.button_count = 0
		self.axis_count = 0
		self.count_3 = 0
		self.count_4 = 0
		self.flags = 0
		self.buttons = ArrayPointer(self.context, self.button_count, generated.formats.logicalcontrols.compound.Button.Button)
		self.axes = ArrayPointer(self.context, self.axis_count, generated.formats.logicalcontrols.compound.AxisValue.AxisValue)
		self.c = ArrayPointer(self.context, self.count_3, )
		self.d = ArrayPointer(self.context, self.count_4, generated.formats.logicalcontrols.compound.Some.Some)
		self.unsure = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.buttons = ArrayPointer.from_stream(stream, instance.context, instance.button_count, generated.formats.logicalcontrols.compound.Button.Button)
		instance.axes = ArrayPointer.from_stream(stream, instance.context, instance.axis_count, generated.formats.logicalcontrols.compound.AxisValue.AxisValue)
		instance.c = ArrayPointer.from_stream(stream, instance.context, instance.count_3, )
		instance.d = ArrayPointer.from_stream(stream, instance.context, instance.count_4, generated.formats.logicalcontrols.compound.Some.Some)
		instance.button_count = stream.read_ubyte()
		instance.axis_count = stream.read_ubyte()
		instance.count_3 = stream.read_ubyte()
		instance.count_4 = stream.read_ubyte()
		instance.flags = stream.read_uint()
		instance.unsure = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.buttons.arg = instance.button_count
		instance.axes.arg = instance.axis_count
		instance.c.arg = instance.count_3
		instance.d.arg = instance.count_4
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
		super()._get_filtered_attribute_list(instance)
		yield ('buttons', ArrayPointer, (instance.button_count, generated.formats.logicalcontrols.compound.Button.Button))
		yield ('axes', ArrayPointer, (instance.axis_count, generated.formats.logicalcontrols.compound.AxisValue.AxisValue))
		yield ('c', ArrayPointer, (instance.count_3, ))
		yield ('d', ArrayPointer, (instance.count_4, generated.formats.logicalcontrols.compound.Some.Some))
		yield ('button_count', Ubyte, (0, None))
		yield ('axis_count', Ubyte, (0, None))
		yield ('count_3', Ubyte, (0, None))
		yield ('count_4', Ubyte, (0, None))
		yield ('flags', Uint, (0, None))
		yield ('unsure', Pointer, (0, generated.formats.base.basic.ZString))

	def get_info_str(self, indent=0):
		return f'LogicalControls [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* buttons = {fmt_member(self.buttons, indent+1)}'
		s += f'\n	* axes = {fmt_member(self.axes, indent+1)}'
		s += f'\n	* c = {fmt_member(self.c, indent+1)}'
		s += f'\n	* d = {fmt_member(self.d, indent+1)}'
		s += f'\n	* button_count = {fmt_member(self.button_count, indent+1)}'
		s += f'\n	* axis_count = {fmt_member(self.axis_count, indent+1)}'
		s += f'\n	* count_3 = {fmt_member(self.count_3, indent+1)}'
		s += f'\n	* count_4 = {fmt_member(self.count_4, indent+1)}'
		s += f'\n	* flags = {fmt_member(self.flags, indent+1)}'
		s += f'\n	* unsure = {fmt_member(self.unsure, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
