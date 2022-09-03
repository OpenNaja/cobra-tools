from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class State(MemStruct):

	"""
	name uncertain
	40 bytes
	"""

	__name__ = 'State'

	_import_path = 'generated.formats.motiongraph.compounds.State'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk = 0
		self.activities_count = 0
		self.count_2 = 0
		self.activities = Pointer(self.context, self.activities_count, State._import_path_map["generated.formats.motiongraph.compounds.PtrList"])
		self.array_2 = Pointer(self.context, self.count_2, State._import_path_map["generated.formats.motiongraph.compounds.TransStructStopList"])
		self.id = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.unk = 0
		self.activities_count = 0
		self.count_2 = 0
		self.activities = Pointer(self.context, self.activities_count, State._import_path_map["generated.formats.motiongraph.compounds.PtrList"])
		self.array_2 = Pointer(self.context, self.count_2, State._import_path_map["generated.formats.motiongraph.compounds.TransStructStopList"])
		self.id = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.unk = Uint.from_stream(stream, instance.context, 0, None)
		instance.activities_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.activities = Pointer.from_stream(stream, instance.context, instance.activities_count, State._import_path_map["generated.formats.motiongraph.compounds.PtrList"])
		instance.count_2 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.array_2 = Pointer.from_stream(stream, instance.context, instance.count_2, State._import_path_map["generated.formats.motiongraph.compounds.TransStructStopList"])
		instance.id = Pointer.from_stream(stream, instance.context, 0, ZString)
		if not isinstance(instance.activities, int):
			instance.activities.arg = instance.activities_count
		if not isinstance(instance.array_2, int):
			instance.array_2.arg = instance.count_2
		if not isinstance(instance.id, int):
			instance.id.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Uint.to_stream(stream, instance.unk)
		Uint.to_stream(stream, instance.activities_count)
		Pointer.to_stream(stream, instance.activities)
		Uint64.to_stream(stream, instance.count_2)
		Pointer.to_stream(stream, instance.array_2)
		Pointer.to_stream(stream, instance.id)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'unk', Uint, (0, None), (False, None)
		yield 'activities_count', Uint, (0, None), (False, None)
		yield 'activities', Pointer, (instance.activities_count, State._import_path_map["generated.formats.motiongraph.compounds.PtrList"]), (False, None)
		yield 'count_2', Uint64, (0, None), (False, None)
		yield 'array_2', Pointer, (instance.count_2, State._import_path_map["generated.formats.motiongraph.compounds.TransStructStopList"]), (False, None)
		yield 'id', Pointer, (0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'State [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* unk = {self.fmt_member(self.unk, indent+1)}'
		s += f'\n	* activities_count = {self.fmt_member(self.activities_count, indent+1)}'
		s += f'\n	* activities = {self.fmt_member(self.activities, indent+1)}'
		s += f'\n	* count_2 = {self.fmt_member(self.count_2, indent+1)}'
		s += f'\n	* array_2 = {self.fmt_member(self.array_2, indent+1)}'
		s += f'\n	* id = {self.fmt_member(self.id, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
