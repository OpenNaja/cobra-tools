from generated.array import Array
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class NextResearch(MemStruct):

	__name__ = 'NextResearch'

	_import_path = 'generated.formats.mechanicresearch.compounds.NextResearch'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_1 = 0
		self.item_name = Array(self.context, 0, ZString, (0,), Pointer)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.unk_1 = 0
		self.item_name = Array(self.context, 0, ZString, (self.arg,), Pointer)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.item_name = Array.from_stream(stream, instance.context, 0, ZString, (instance.arg,), Pointer)
		instance.unk_1 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.item_name, int):
			instance.item_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.item_name, instance.context, 0, ZString, (instance.arg,), Pointer)
		Uint64.to_stream(stream, instance.unk_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'item_name', Array, (0, ZString, (instance.arg,), Pointer), (False, None)
		yield 'unk_1', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'NextResearch [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
