from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ThirdFrag(MemStruct):

	"""
	72 bytes
	"""

	__name__ = 'ThirdFrag'

	_import_path = 'generated.formats.motiongraph.compounds.ThirdFrag'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.count_3 = 0
		self.count_4 = 0
		self.lua_method = Pointer(self.context, 0, ZString)
		self.ptr_1 = Pointer(self.context, 0, ThirdFrag._import_path_map["generated.formats.motiongraph.compounds.TwoPtrFirst"])
		self.ptr_2 = Pointer(self.context, 0, ThirdFrag._import_path_map["generated.formats.motiongraph.compounds.Sixtyfour"])
		self.member = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.count_3 = 0
		self.count_4 = 0
		self.lua_method = Pointer(self.context, 0, ZString)
		self.ptr_1 = Pointer(self.context, 0, ThirdFrag._import_path_map["generated.formats.motiongraph.compounds.TwoPtrFirst"])
		self.ptr_2 = Pointer(self.context, 0, ThirdFrag._import_path_map["generated.formats.motiongraph.compounds.Sixtyfour"])
		self.member = Pointer(self.context, 0, ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.lua_method = Pointer.from_stream(stream, instance.context, 0, ZString)
		instance.count_0 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.count_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.ptr_1 = Pointer.from_stream(stream, instance.context, 0, ThirdFrag._import_path_map["generated.formats.motiongraph.compounds.TwoPtrFirst"])
		instance.count_2 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.count_3 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.ptr_2 = Pointer.from_stream(stream, instance.context, 0, ThirdFrag._import_path_map["generated.formats.motiongraph.compounds.Sixtyfour"])
		instance.count_4 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.member = Pointer.from_stream(stream, instance.context, 0, ZString)
		if not isinstance(instance.lua_method, int):
			instance.lua_method.arg = 0
		if not isinstance(instance.ptr_1, int):
			instance.ptr_1.arg = 0
		if not isinstance(instance.ptr_2, int):
			instance.ptr_2.arg = 0
		if not isinstance(instance.member, int):
			instance.member.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.lua_method)
		Uint64.to_stream(stream, instance.count_0)
		Uint64.to_stream(stream, instance.count_1)
		Pointer.to_stream(stream, instance.ptr_1)
		Uint64.to_stream(stream, instance.count_2)
		Uint64.to_stream(stream, instance.count_3)
		Pointer.to_stream(stream, instance.ptr_2)
		Uint64.to_stream(stream, instance.count_4)
		Pointer.to_stream(stream, instance.member)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'lua_method', Pointer, (0, ZString), (False, None)
		yield 'count_0', Uint64, (0, None), (False, None)
		yield 'count_1', Uint64, (0, None), (False, None)
		yield 'ptr_1', Pointer, (0, ThirdFrag._import_path_map["generated.formats.motiongraph.compounds.TwoPtrFirst"]), (False, None)
		yield 'count_2', Uint64, (0, None), (False, None)
		yield 'count_3', Uint64, (0, None), (False, None)
		yield 'ptr_2', Pointer, (0, ThirdFrag._import_path_map["generated.formats.motiongraph.compounds.Sixtyfour"]), (False, None)
		yield 'count_4', Uint64, (0, None), (False, None)
		yield 'member', Pointer, (0, ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'ThirdFrag [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* lua_method = {self.fmt_member(self.lua_method, indent+1)}'
		s += f'\n	* count_0 = {self.fmt_member(self.count_0, indent+1)}'
		s += f'\n	* count_1 = {self.fmt_member(self.count_1, indent+1)}'
		s += f'\n	* ptr_1 = {self.fmt_member(self.ptr_1, indent+1)}'
		s += f'\n	* count_2 = {self.fmt_member(self.count_2, indent+1)}'
		s += f'\n	* count_3 = {self.fmt_member(self.count_3, indent+1)}'
		s += f'\n	* ptr_2 = {self.fmt_member(self.ptr_2, indent+1)}'
		s += f'\n	* count_4 = {self.fmt_member(self.count_4, indent+1)}'
		s += f'\n	* member = {self.fmt_member(self.member, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
