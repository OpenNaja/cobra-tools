import generated.formats.base.basic
import generated.formats.mergedetails.compound.PtrList
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class MergedetailsRoot(MemStruct):

	"""
	48 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero_0 = 0
		self.zero_1 = 0
		self.count = 0
		self.flag = 0
		self.merge_names = 0
		self.queries = 0
		self.field_name = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.zero_0 = 0
		self.zero_1 = 0
		self.count = 0
		self.flag = 0
		self.merge_names = Pointer(self.context, self.count, generated.formats.mergedetails.compound.PtrList.PtrList)
		self.queries = Pointer(self.context, self.count, generated.formats.mergedetails.compound.PtrList.PtrList)
		self.field_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.merge_names = Pointer.from_stream(stream, instance.context, instance.count, generated.formats.mergedetails.compound.PtrList.PtrList)
		instance.zero_0 = stream.read_uint64()
		instance.zero_1 = stream.read_uint64()
		instance.queries = Pointer.from_stream(stream, instance.context, instance.count, generated.formats.mergedetails.compound.PtrList.PtrList)
		instance.field_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.count = stream.read_uint()
		instance.flag = stream.read_uint()
		instance.merge_names.arg = instance.count
		instance.queries.arg = instance.count
		instance.field_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.merge_names)
		stream.write_uint64(instance.zero_0)
		stream.write_uint64(instance.zero_1)
		Pointer.to_stream(stream, instance.queries)
		Pointer.to_stream(stream, instance.field_name)
		stream.write_uint(instance.count)
		stream.write_uint(instance.flag)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('merge_names', Pointer, (instance.count, generated.formats.mergedetails.compound.PtrList.PtrList))
		yield ('zero_0', Uint64, (0, None))
		yield ('zero_1', Uint64, (0, None))
		yield ('queries', Pointer, (instance.count, generated.formats.mergedetails.compound.PtrList.PtrList))
		yield ('field_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('count', Uint, (0, None))
		yield ('flag', Uint, (0, None))

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
