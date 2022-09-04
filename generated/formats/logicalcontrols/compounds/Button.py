from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Button(MemStruct):

	__name__ = 'Button'

	_import_path = 'generated.formats.logicalcontrols.compounds.Button'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.datas_count = 0
		self.flags = 0
		self.button_name = Pointer(self.context, 0, ZString)
		self.datas = ArrayPointer(self.context, self.datas_count, Button._import_path_map["generated.formats.logicalcontrols.compounds.ButtonData"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.datas_count = 0
		self.flags = 0
		self.button_name = Pointer(self.context, 0, ZString)
		self.datas = ArrayPointer(self.context, self.datas_count, Button._import_path_map["generated.formats.logicalcontrols.compounds.ButtonData"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.button_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.datas = ArrayPointer.from_stream(stream, instance.context, instance.datas_count, Button._import_path_map["generated.formats.logicalcontrols.compounds.ButtonData"])
		instance.datas_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.flags = Uint.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.button_name, int):
			instance.button_name.arg = 0
		if not isinstance(instance.datas, int):
			instance.datas.arg = instance.datas_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.button_name)
		ArrayPointer.to_stream(stream, instance.datas)
		Uint.to_stream(stream, instance.datas_count)
		Uint.to_stream(stream, instance.flags)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'button_name', Pointer, (0, ZString), (False, None)
		yield 'datas', ArrayPointer, (instance.datas_count, Button._import_path_map["generated.formats.logicalcontrols.compounds.ButtonData"]), (False, None)
		yield 'datas_count', Uint, (0, None), (False, None)
		yield 'flags', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Button [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
