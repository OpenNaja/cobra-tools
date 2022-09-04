from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class LogicalControls(MemStruct):

	__name__ = 'LogicalControls'

	_import_path = 'generated.formats.logicalcontrols.compounds.LogicalControls'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.button_count = 0
		self.axis_count = 0
		self.count_3 = 0
		self.count_4 = 0
		self.flags = 0
		self.buttons = ArrayPointer(self.context, self.button_count, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.Button"])
		self.axes = ArrayPointer(self.context, self.axis_count, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.AxisValue"])
		self.axis_buttons = ArrayPointer(self.context, self.count_3, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.AxisButton"])
		self.d = ArrayPointer(self.context, self.count_4, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.Some"])
		self.unsure = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.button_count = 0
		self.axis_count = 0
		self.count_3 = 0
		self.count_4 = 0
		self.flags = 0
		self.buttons = ArrayPointer(self.context, self.button_count, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.Button"])
		self.axes = ArrayPointer(self.context, self.axis_count, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.AxisValue"])
		self.axis_buttons = ArrayPointer(self.context, self.count_3, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.AxisButton"])
		self.d = ArrayPointer(self.context, self.count_4, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.Some"])
		self.unsure = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.buttons = ArrayPointer.from_stream(stream, instance.context, instance.button_count, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.Button"])
		instance.axes = ArrayPointer.from_stream(stream, instance.context, instance.axis_count, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.AxisValue"])
		instance.axis_buttons = ArrayPointer.from_stream(stream, instance.context, instance.count_3, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.AxisButton"])
		instance.d = ArrayPointer.from_stream(stream, instance.context, instance.count_4, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.Some"])
		instance.button_count = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.axis_count = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_3 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.count_4 = Ubyte.from_stream(stream, instance.context, 0, None)
		instance.flags = Uint.from_stream(stream, instance.context, 0, None)
		instance.unsure = Pointer.from_stream(stream, instance.context, 0, ZString)
		if not isinstance(instance.buttons, int):
			instance.buttons.arg = instance.button_count
		if not isinstance(instance.axes, int):
			instance.axes.arg = instance.axis_count
		if not isinstance(instance.axis_buttons, int):
			instance.axis_buttons.arg = instance.count_3
		if not isinstance(instance.d, int):
			instance.d.arg = instance.count_4
		if not isinstance(instance.unsure, int):
			instance.unsure.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		ArrayPointer.to_stream(stream, instance.buttons)
		ArrayPointer.to_stream(stream, instance.axes)
		ArrayPointer.to_stream(stream, instance.axis_buttons)
		ArrayPointer.to_stream(stream, instance.d)
		Ubyte.to_stream(stream, instance.button_count)
		Ubyte.to_stream(stream, instance.axis_count)
		Ubyte.to_stream(stream, instance.count_3)
		Ubyte.to_stream(stream, instance.count_4)
		Uint.to_stream(stream, instance.flags)
		Pointer.to_stream(stream, instance.unsure)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'buttons', ArrayPointer, (instance.button_count, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.Button"]), (False, None)
		yield 'axes', ArrayPointer, (instance.axis_count, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.AxisValue"]), (False, None)
		yield 'axis_buttons', ArrayPointer, (instance.count_3, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.AxisButton"]), (False, None)
		yield 'd', ArrayPointer, (instance.count_4, LogicalControls._import_path_map["generated.formats.logicalcontrols.compounds.Some"]), (False, None)
		yield 'button_count', Ubyte, (0, None), (False, None)
		yield 'axis_count', Ubyte, (0, None), (False, None)
		yield 'count_3', Ubyte, (0, None), (False, None)
		yield 'count_4', Ubyte, (0, None), (False, None)
		yield 'flags', Uint, (0, None), (False, None)
		yield 'unsure', Pointer, (0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'LogicalControls [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
