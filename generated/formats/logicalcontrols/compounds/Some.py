from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.ArrayPointer import ArrayPointer
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Some(MemStruct):

	"""
	24 bytes
	"""

	__name__ = 'Some'

	_import_path = 'generated.formats.logicalcontrols.compounds.Some'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.some_count = 0
		self.some_name = Pointer(self.context, 0, ZString)
		self.some_data = ArrayPointer(self.context, self.some_count, Some._import_path_map["generated.formats.logicalcontrols.compounds.SomeData"])
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.some_count = 0
		self.some_name = Pointer(self.context, 0, ZString)
		self.some_data = ArrayPointer(self.context, self.some_count, Some._import_path_map["generated.formats.logicalcontrols.compounds.SomeData"])

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.some_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.some_data = ArrayPointer.from_stream(stream, instance.context, instance.some_count, Some._import_path_map["generated.formats.logicalcontrols.compounds.SomeData"])
		instance.some_count = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.some_name, int):
			instance.some_name.arg = 0
		if not isinstance(instance.some_data, int):
			instance.some_data.arg = instance.some_count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.some_name)
		ArrayPointer.to_stream(stream, instance.some_data)
		Uint64.to_stream(stream, instance.some_count)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'some_name', Pointer, (0, ZString), (False, None)
		yield 'some_data', ArrayPointer, (instance.some_count, Some._import_path_map["generated.formats.logicalcontrols.compounds.SomeData"]), (False, None)
		yield 'some_count', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Some [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
