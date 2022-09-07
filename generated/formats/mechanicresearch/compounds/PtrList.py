from generated.array import Array
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PtrList(MemStruct):

	__name__ = 'PtrList'

	_import_path = 'generated.formats.mechanicresearch.compounds.PtrList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptrs = Array(self.context, 0, ZString, (0,), Pointer)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.ptrs = Array(self.context, 0, ZString, (self.arg,), Pointer)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.ptrs = Array.from_stream(stream, instance.context, 0, ZString, (instance.arg,), Pointer)
		if not isinstance(instance.ptrs, int):
			instance.ptrs.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.ptrs, instance.context, 0, ZString, (instance.arg,), Pointer)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ptrs', Array, (0, ZString, (instance.arg,), Pointer), (False, None)

	def get_info_str(self, indent=0):
		return f'PtrList [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
