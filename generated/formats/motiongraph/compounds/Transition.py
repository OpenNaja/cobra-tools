import generated.formats.base.basic
import generated.formats.motiongraph.compounds.PtrList
import generated.formats.motiongraph.compounds.TransStructArray
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class Transition(MemStruct):

	"""
	40 bytes
	only used if transition is in 'id'
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.ptr_0 = Pointer(self.context, self.count_1, generated.formats.motiongraph.compounds.PtrList.PtrList)
		self.ptr_1 = Pointer(self.context, self.count_2, generated.formats.motiongraph.compounds.TransStructArray.TransStructArray)
		self.id = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.ptr_0 = Pointer(self.context, self.count_1, generated.formats.motiongraph.compounds.PtrList.PtrList)
		self.ptr_1 = Pointer(self.context, self.count_2, generated.formats.motiongraph.compounds.TransStructArray.TransStructArray)
		self.id = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.count_0 = stream.read_uint()
		instance.count_1 = stream.read_uint()
		instance.ptr_0 = Pointer.from_stream(stream, instance.context, instance.count_1, generated.formats.motiongraph.compounds.PtrList.PtrList)
		instance.count_2 = stream.read_uint64()
		instance.ptr_1 = Pointer.from_stream(stream, instance.context, instance.count_2, generated.formats.motiongraph.compounds.TransStructArray.TransStructArray)
		instance.id = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		if not isinstance(instance.ptr_0, int):
			instance.ptr_0.arg = instance.count_1
		if not isinstance(instance.ptr_1, int):
			instance.ptr_1.arg = instance.count_2
		if not isinstance(instance.id, int):
			instance.id.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.count_0)
		stream.write_uint(instance.count_1)
		Pointer.to_stream(stream, instance.ptr_0)
		stream.write_uint64(instance.count_2)
		Pointer.to_stream(stream, instance.ptr_1)
		Pointer.to_stream(stream, instance.id)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'count_0', Uint, (0, None)
		yield 'count_1', Uint, (0, None)
		yield 'ptr_0', Pointer, (instance.count_1, generated.formats.motiongraph.compounds.PtrList.PtrList)
		yield 'count_2', Uint64, (0, None)
		yield 'ptr_1', Pointer, (instance.count_2, generated.formats.motiongraph.compounds.TransStructArray.TransStructArray)
		yield 'id', Pointer, (0, generated.formats.base.basic.ZString)

	def get_info_str(self, indent=0):
		return f'Transition [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* count_0 = {self.fmt_member(self.count_0, indent+1)}'
		s += f'\n	* count_1 = {self.fmt_member(self.count_1, indent+1)}'
		s += f'\n	* ptr_0 = {self.fmt_member(self.ptr_0, indent+1)}'
		s += f'\n	* count_2 = {self.fmt_member(self.count_2, indent+1)}'
		s += f'\n	* ptr_1 = {self.fmt_member(self.ptr_1, indent+1)}'
		s += f'\n	* id = {self.fmt_member(self.id, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
