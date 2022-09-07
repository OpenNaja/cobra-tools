from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class AxisButton(MemStruct):

	"""
	24 bytes, can be padded to 32
	"""

	__name__ = 'AxisButton'

	_import_path = 'generated.formats.logicalcontrols.compounds.AxisButton'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.button_name = Pointer(self.context, 0, ZString)
		self.axis_name_x = Pointer(self.context, 0, ZString)
		self.axis_name_y = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.button_name = Pointer(self.context, 0, ZString)
		self.axis_name_x = Pointer(self.context, 0, ZString)
		self.axis_name_y = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.button_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.axis_name_x = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.axis_name_y = Pointer.from_stream(stream, instance.context, 0, ZString)
		if not isinstance(instance.button_name, int):
			instance.button_name.arg = 0
		if not isinstance(instance.axis_name_x, int):
			instance.axis_name_x.arg = 0
		if not isinstance(instance.axis_name_y, int):
			instance.axis_name_y.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.button_name)
		Pointer.to_stream(stream, instance.axis_name_x)
		Pointer.to_stream(stream, instance.axis_name_y)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'button_name', Pointer, (0, ZString), (False, None)
		yield 'axis_name_x', Pointer, (0, ZString), (False, None)
		yield 'axis_name_y', Pointer, (0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'AxisButton [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
