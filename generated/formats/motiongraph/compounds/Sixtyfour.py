from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Sixtyfour(MemStruct):

	"""
	64 bytes
	"""

	__name__ = 'Sixtyfour'

	_import_path = 'generated.formats.motiongraph.compounds.Sixtyfour'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.count_3 = 0
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ptr_1 = Pointer(self.context, 0, None)
		self.ptr_2 = Pointer(self.context, 0, None)
		self.ptr_3 = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.count_3 = 0
		self.ptr_0 = Pointer(self.context, 0, None)
		self.ptr_1 = Pointer(self.context, 0, None)
		self.ptr_2 = Pointer(self.context, 0, None)
		self.ptr_3 = Pointer(self.context, 0, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.count_0 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.ptr_0 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_1 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.count_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.count_2 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.ptr_2 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.ptr_3 = Pointer.from_stream(stream, instance.context, 0, None)
		instance.count_3 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.ptr_0, int):
			instance.ptr_0.arg = 0
		if not isinstance(instance.ptr_1, int):
			instance.ptr_1.arg = 0
		if not isinstance(instance.ptr_2, int):
			instance.ptr_2.arg = 0
		if not isinstance(instance.ptr_3, int):
			instance.ptr_3.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint64.to_stream(stream, instance.count_0)
		Pointer.to_stream(stream, instance.ptr_0)
		Pointer.to_stream(stream, instance.ptr_1)
		Uint64.to_stream(stream, instance.count_1)
		Uint64.to_stream(stream, instance.count_2)
		Pointer.to_stream(stream, instance.ptr_2)
		Pointer.to_stream(stream, instance.ptr_3)
		Uint64.to_stream(stream, instance.count_3)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'count_0', Uint64, (0, None), (False, None)
		yield 'ptr_0', Pointer, (0, None), (False, None)
		yield 'ptr_1', Pointer, (0, None), (False, None)
		yield 'count_1', Uint64, (0, None), (False, None)
		yield 'count_2', Uint64, (0, None), (False, None)
		yield 'ptr_2', Pointer, (0, None), (False, None)
		yield 'ptr_3', Pointer, (0, None), (False, None)
		yield 'count_3', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'Sixtyfour [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* count_0 = {self.fmt_member(self.count_0, indent+1)}'
		s += f'\n	* ptr_0 = {self.fmt_member(self.ptr_0, indent+1)}'
		s += f'\n	* ptr_1 = {self.fmt_member(self.ptr_1, indent+1)}'
		s += f'\n	* count_1 = {self.fmt_member(self.count_1, indent+1)}'
		s += f'\n	* count_2 = {self.fmt_member(self.count_2, indent+1)}'
		s += f'\n	* ptr_2 = {self.fmt_member(self.ptr_2, indent+1)}'
		s += f'\n	* ptr_3 = {self.fmt_member(self.ptr_3, indent+1)}'
		s += f'\n	* count_3 = {self.fmt_member(self.count_3, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
