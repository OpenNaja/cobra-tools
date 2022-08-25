import generated.formats.enumnamer.compounds.PtrList
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class EnumnamerRoot(MemStruct):

	__name__ = EnumnamerRoot

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count = 0
		self.strings = Pointer(self.context, self.count, generated.formats.enumnamer.compounds.PtrList.PtrList)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count = 0
		self.strings = Pointer(self.context, self.count, generated.formats.enumnamer.compounds.PtrList.PtrList)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.count = Uint64.from_stream(stream, instance.context, 0, None)
		instance.strings = Pointer.from_stream(stream, instance.context, instance.count, generated.formats.enumnamer.compounds.PtrList.PtrList)
		if not isinstance(instance.strings, int):
			instance.strings.arg = instance.count

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.count)
		Pointer.to_stream(stream, instance.strings)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'count', Uint64, (0, None), (False, None)
		yield 'strings', Pointer, (instance.count, generated.formats.enumnamer.compounds.PtrList.PtrList), (False, None)

	def get_info_str(self, indent=0):
		return f'EnumnamerRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* count = {self.fmt_member(self.count, indent+1)}'
		s += f'\n	* strings = {self.fmt_member(self.strings, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
