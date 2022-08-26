from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.mergedetails.compounds.PtrList import PtrList
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MergedetailsRoot(MemStruct):

	"""
	48 bytes
	"""

	__name__ = 'MergedetailsRoot'

	_import_path = 'generated.formats.mergedetails.compounds.MergedetailsRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero_0 = 0
		self.zero_1 = 0
		self.count = 0
		self.flag = 0
		self.merge_names = Pointer(self.context, self.count, PtrList)
		self.queries = Pointer(self.context, self.count, PtrList)
		self.field_name = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.zero_0 = 0
		self.zero_1 = 0
		self.count = 0
		self.flag = 0
		self.merge_names = Pointer(self.context, self.count, PtrList)
		self.queries = Pointer(self.context, self.count, PtrList)
		self.field_name = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.merge_names = Pointer.from_stream(stream, instance.context, instance.count, PtrList)
		instance.zero_0 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.zero_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.queries = Pointer.from_stream(stream, instance.context, instance.count, PtrList)
		instance.field_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.count = Uint.from_stream(stream, instance.context, 0, None)
		instance.flag = Uint.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.merge_names, int):
			instance.merge_names.arg = instance.count
		if not isinstance(instance.queries, int):
			instance.queries.arg = instance.count
		if not isinstance(instance.field_name, int):
			instance.field_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.merge_names)
		Uint64.to_stream(stream, instance.zero_0)
		Uint64.to_stream(stream, instance.zero_1)
		Pointer.to_stream(stream, instance.queries)
		Pointer.to_stream(stream, instance.field_name)
		Uint.to_stream(stream, instance.count)
		Uint.to_stream(stream, instance.flag)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'merge_names', Pointer, (instance.count, PtrList), (False, None)
		yield 'zero_0', Uint64, (0, None), (False, None)
		yield 'zero_1', Uint64, (0, None), (False, None)
		yield 'queries', Pointer, (instance.count, PtrList), (False, None)
		yield 'field_name', Pointer, (0, ZString), (False, None)
		yield 'count', Uint, (0, None), (False, None)
		yield 'flag', Uint, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'MergedetailsRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* merge_names = {self.fmt_member(self.merge_names, indent+1)}'
		s += f'\n	* zero_0 = {self.fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* zero_1 = {self.fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* queries = {self.fmt_member(self.queries, indent+1)}'
		s += f'\n	* field_name = {self.fmt_member(self.field_name, indent+1)}'
		s += f'\n	* count = {self.fmt_member(self.count, indent+1)}'
		s += f'\n	* flag = {self.fmt_member(self.flag, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
