from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TrackElementData(MemStruct):

	"""
	PC: 80
	"""

	__name__ = 'TrackElementData'

	_import_path = 'generated.formats.trackelement.compounds.TrackElementData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_0 = 0
		self.unk_1 = 0
		self.unk_2 = 0
		self.unk_3 = 32
		self.unk_4 = 1024
		self.unk_5 = 1
		self.unk_6 = 1
		self.unk_7 = 0
		self.loop_name = Pointer(self.context, 0, ZString)
		self.ovl_name = Pointer(self.context, 0, ZString)
		self.catwalk = Pointer(self.context, 0, TrackElementData._import_path_map["generated.formats.trackelement.compounds.TrackElementSub"])
		self.optional_catwalk = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.unk_0 = 0
		self.unk_1 = 0
		self.unk_2 = 0
		self.unk_3 = 32
		self.unk_4 = 1024
		self.unk_5 = 1
		self.unk_6 = 1
		self.unk_7 = 0
		self.loop_name = Pointer(self.context, 0, ZString)
		self.ovl_name = Pointer(self.context, 0, ZString)
		self.catwalk = Pointer(self.context, 0, TrackElementData._import_path_map["generated.formats.trackelement.compounds.TrackElementSub"])
		self.optional_catwalk = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.loop_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.ovl_name = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.catwalk = Pointer.from_stream(stream, instance.context, 0, TrackElementData._import_path_map["generated.formats.trackelement.compounds.TrackElementSub"])
		instance.unk_0 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.optional_catwalk = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.unk_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.unk_2 = Ushort.from_stream(stream, instance.context, 0, None)
		instance.unk_3 = Ushort.from_stream(stream, instance.context, 0, None)
		instance.unk_4 = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk_5 = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk_6 = Uint.from_stream(stream, instance.context, 0, None)
		instance.unk_7 = Uint64.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.loop_name, int):
			instance.loop_name.arg = 0
		if not isinstance(instance.ovl_name, int):
			instance.ovl_name.arg = 0
		if not isinstance(instance.catwalk, int):
			instance.catwalk.arg = 0
		if not isinstance(instance.optional_catwalk, int):
			instance.optional_catwalk.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.loop_name)
		Pointer.to_stream(stream, instance.ovl_name)
		Pointer.to_stream(stream, instance.catwalk)
		Uint64.to_stream(stream, instance.unk_0)
		Pointer.to_stream(stream, instance.optional_catwalk)
		Uint64.to_stream(stream, instance.unk_1)
		Ushort.to_stream(stream, instance.unk_2)
		Ushort.to_stream(stream, instance.unk_3)
		Uint.to_stream(stream, instance.unk_4)
		Uint.to_stream(stream, instance.unk_5)
		Uint.to_stream(stream, instance.unk_6)
		Uint64.to_stream(stream, instance.unk_7)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'loop_name', Pointer, (0, ZString), (False, None)
		yield 'ovl_name', Pointer, (0, ZString), (False, None)
		yield 'catwalk', Pointer, (0, TrackElementData._import_path_map["generated.formats.trackelement.compounds.TrackElementSub"]), (False, None)
		yield 'unk_0', Uint64, (0, None), (False, None)
		yield 'optional_catwalk', Pointer, (0, ZString), (False, None)
		yield 'unk_1', Uint64, (0, None), (False, None)
		yield 'unk_2', Ushort, (0, None), (False, 0)
		yield 'unk_3', Ushort, (0, None), (False, 32)
		yield 'unk_4', Uint, (0, None), (False, 1024)
		yield 'unk_5', Uint, (0, None), (False, 1)
		yield 'unk_6', Uint, (0, None), (False, 1)
		yield 'unk_7', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'TrackElementData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* loop_name = {self.fmt_member(self.loop_name, indent+1)}'
		s += f'\n	* ovl_name = {self.fmt_member(self.ovl_name, indent+1)}'
		s += f'\n	* catwalk = {self.fmt_member(self.catwalk, indent+1)}'
		s += f'\n	* unk_0 = {self.fmt_member(self.unk_0, indent+1)}'
		s += f'\n	* optional_catwalk = {self.fmt_member(self.optional_catwalk, indent+1)}'
		s += f'\n	* unk_1 = {self.fmt_member(self.unk_1, indent+1)}'
		s += f'\n	* unk_2 = {self.fmt_member(self.unk_2, indent+1)}'
		s += f'\n	* unk_3 = {self.fmt_member(self.unk_3, indent+1)}'
		s += f'\n	* unk_4 = {self.fmt_member(self.unk_4, indent+1)}'
		s += f'\n	* unk_5 = {self.fmt_member(self.unk_5, indent+1)}'
		s += f'\n	* unk_6 = {self.fmt_member(self.unk_6, indent+1)}'
		s += f'\n	* unk_7 = {self.fmt_member(self.unk_7, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
