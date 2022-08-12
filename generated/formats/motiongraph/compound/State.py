from generated.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.motiongraph.compound.PtrList
import generated.formats.motiongraph.compound.TransStructStopList
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class State(MemStruct):

	"""
	name uncertain
	40 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default)
		self.unk = 0
		self.activities_count = 0
		self.count_2 = 0
		self.activities = 0
		self.array_2 = 0
		self.id = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.unk = 0
		self.activities_count = 0
		self.count_2 = 0
		self.activities = Pointer(self.context, self.activities_count, generated.formats.motiongraph.compound.PtrList.PtrList)
		self.array_2 = Pointer(self.context, self.count_2, generated.formats.motiongraph.compound.TransStructStopList.TransStructStopList)
		self.id = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.unk = stream.read_uint()
		instance.activities_count = stream.read_uint()
		instance.activities = Pointer.from_stream(stream, instance.context, instance.activities_count, generated.formats.motiongraph.compound.PtrList.PtrList)
		instance.count_2 = stream.read_uint64()
		instance.array_2 = Pointer.from_stream(stream, instance.context, instance.count_2, generated.formats.motiongraph.compound.TransStructStopList.TransStructStopList)
		instance.id = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.activities.arg = instance.activities_count
		instance.array_2.arg = instance.count_2
		instance.id.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.unk)
		stream.write_uint(instance.activities_count)
		Pointer.to_stream(stream, instance.activities)
		stream.write_uint64(instance.count_2)
		Pointer.to_stream(stream, instance.array_2)
		Pointer.to_stream(stream, instance.id)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('unk', Uint, (0, None))
		yield ('activities_count', Uint, (0, None))
		yield ('activities', Pointer, (instance.activities_count, generated.formats.motiongraph.compound.PtrList.PtrList))
		yield ('count_2', Uint64, (0, None))
		yield ('array_2', Pointer, (instance.count_2, generated.formats.motiongraph.compound.TransStructStopList.TransStructStopList))
		yield ('id', Pointer, (0, generated.formats.base.basic.ZString))

	def get_info_str(self, indent=0):
		return f'State [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* unk = {fmt_member(self.unk, indent+1)}'
		s += f'\n	* activities_count = {fmt_member(self.activities_count, indent+1)}'
		s += f'\n	* activities = {fmt_member(self.activities, indent+1)}'
		s += f'\n	* count_2 = {fmt_member(self.count_2, indent+1)}'
		s += f'\n	* array_2 = {fmt_member(self.array_2, indent+1)}'
		s += f'\n	* id = {fmt_member(self.id, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
