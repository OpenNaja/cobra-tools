from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class LogicalControls(MemStruct):

	__name__ = 'LogicalControls'

	_import_key = 'logicalcontrols.compounds.LogicalControls'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.button_count = 0
		self.axis_count = 0
		self.count_3 = 0
		self.count_4 = 0
		self.flags = 0
		self.buttons = ArrayPointer(self.context, self.button_count, LogicalControls._import_map["logicalcontrols.compounds.Button"])
		self.axes = ArrayPointer(self.context, self.axis_count, LogicalControls._import_map["logicalcontrols.compounds.AxisValue"])
		self.axis_buttons = ArrayPointer(self.context, self.count_3, LogicalControls._import_map["logicalcontrols.compounds.AxisButton"])
		self.d = ArrayPointer(self.context, self.count_4, LogicalControls._import_map["logicalcontrols.compounds.Some"])
		self.unsure = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('buttons', ArrayPointer, (None, None), (False, None), None),
		('axes', ArrayPointer, (None, None), (False, None), None),
		('axis_buttons', ArrayPointer, (None, None), (False, None), None),
		('d', ArrayPointer, (None, None), (False, None), None),
		('button_count', Ubyte, (0, None), (False, None), None),
		('axis_count', Ubyte, (0, None), (False, None), None),
		('count_3', Ubyte, (0, None), (False, None), None),
		('count_4', Ubyte, (0, None), (False, None), None),
		('flags', Uint, (0, None), (False, None), None),
		('unsure', Pointer, (0, ZString), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'buttons', ArrayPointer, (instance.button_count, LogicalControls._import_map["logicalcontrols.compounds.Button"]), (False, None)
		yield 'axes', ArrayPointer, (instance.axis_count, LogicalControls._import_map["logicalcontrols.compounds.AxisValue"]), (False, None)
		yield 'axis_buttons', ArrayPointer, (instance.count_3, LogicalControls._import_map["logicalcontrols.compounds.AxisButton"]), (False, None)
		yield 'd', ArrayPointer, (instance.count_4, LogicalControls._import_map["logicalcontrols.compounds.Some"]), (False, None)
		yield 'button_count', Ubyte, (0, None), (False, None)
		yield 'axis_count', Ubyte, (0, None), (False, None)
		yield 'count_3', Ubyte, (0, None), (False, None)
		yield 'count_4', Ubyte, (0, None), (False, None)
		yield 'flags', Uint, (0, None), (False, None)
		yield 'unsure', Pointer, (0, ZString), (False, None)
