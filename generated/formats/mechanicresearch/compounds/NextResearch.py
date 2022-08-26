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
		self.item_name = Array((0,), Pointer, self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.unk_1 = 0
		self.item_name = Array((self.arg,), Pointer, self.context, 0, ZString)

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
		Array.to_stream(stream, instance.item_name, (instance.arg,), Pointer, instance.context, 0, ZString)
		Uint64.to_stream(stream, instance.unk_1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'item_name', Array, ((instance.arg,), Pointer, 0, ZString), (False, None)
		yield 'unk_1', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'NextResearch [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* item_name = {self.fmt_member(self.item_name, indent+1)}'
		s += f'\n	* unk_1 = {self.fmt_member(self.unk_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
