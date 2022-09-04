from generated.array import Array
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class PtrList(MemStruct):

	__name__ = 'PtrList'

	_import_path = 'generated.formats.specdef.compounds.PtrList'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ptrs = Array((0,), Pointer, self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.ptrs = Array((self.arg,), Pointer, self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.ptrs = Array.from_stream(stream, instance.context, 0, ZString, (instance.arg,), Pointer)
		if not isinstance(instance.ptrs, int):
			instance.ptrs.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Array.to_stream(stream, instance.ptrs, (instance.arg,), Pointer, instance.context, 0, ZString)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'ptrs', Array, ((instance.arg,), Pointer, 0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'PtrList [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* ptrs = {self.fmt_member(self.ptrs, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
