import generated.formats.base.basic
import generated.formats.motiongraph.compounds.LuaModules
import generated.formats.motiongraph.compounds.MGTwo
import generated.formats.motiongraph.compounds.MRFMember1
import generated.formats.motiongraph.compounds.MRFMember2
import generated.formats.motiongraph.compounds.MotiongraphRootFrag
import generated.formats.motiongraph.compounds.StateArray
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MotiongraphHeader(MemStruct):

	"""
	# if self.ovl.context.version > 47:
	"""

	__name__ = 'MotiongraphHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_0 = 0
		self.count_1 = 0
		self.ptr_0 = Pointer(self.context, 0, generated.formats.motiongraph.compounds.MotiongraphRootFrag.MotiongraphRootFrag)
		self.state_output_entries = Pointer(self.context, 0, generated.formats.motiongraph.compounds.StateArray.StateArray)
		self.ptr_2 = Pointer(self.context, 0, generated.formats.motiongraph.compounds.MGTwo.MGTwo)
		self.ptr_3 = Pointer(self.context, 0, generated.formats.motiongraph.compounds.MRFMember1.MRFMember1)
		self.lua_modules = Pointer(self.context, 0, generated.formats.motiongraph.compounds.LuaModules.LuaModules)
		self.lua_results = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.first_non_transition_state = Pointer(self.context, 0, generated.formats.motiongraph.compounds.MRFMember2.MRFMember2)
		self.empty_str = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.count_0 = 0
		self.count_1 = 0
		self.ptr_0 = Pointer(self.context, 0, generated.formats.motiongraph.compounds.MotiongraphRootFrag.MotiongraphRootFrag)
		self.state_output_entries = Pointer(self.context, 0, generated.formats.motiongraph.compounds.StateArray.StateArray)
		self.ptr_2 = Pointer(self.context, 0, generated.formats.motiongraph.compounds.MGTwo.MGTwo)
		self.ptr_3 = Pointer(self.context, 0, generated.formats.motiongraph.compounds.MRFMember1.MRFMember1)
		self.lua_modules = Pointer(self.context, 0, generated.formats.motiongraph.compounds.LuaModules.LuaModules)
		self.lua_results = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.first_non_transition_state = Pointer(self.context, 0, generated.formats.motiongraph.compounds.MRFMember2.MRFMember2)
		self.empty_str = Pointer(self.context, 0, generated.formats.base.basic.ZString)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.ptr_0 = Pointer.from_stream(stream, instance.context, 0, generated.formats.motiongraph.compounds.MotiongraphRootFrag.MotiongraphRootFrag)
		instance.state_output_entries = Pointer.from_stream(stream, instance.context, 0, generated.formats.motiongraph.compounds.StateArray.StateArray)
		instance.ptr_2 = Pointer.from_stream(stream, instance.context, 0, generated.formats.motiongraph.compounds.MGTwo.MGTwo)
		instance.ptr_3 = Pointer.from_stream(stream, instance.context, 0, generated.formats.motiongraph.compounds.MRFMember1.MRFMember1)
		instance.count_0 = Uint.from_stream(stream, instance.context, 0, None)
		instance.count_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.lua_modules = Pointer.from_stream(stream, instance.context, 0, generated.formats.motiongraph.compounds.LuaModules.LuaModules)
		instance.lua_results = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.first_non_transition_state = Pointer.from_stream(stream, instance.context, 0, generated.formats.motiongraph.compounds.MRFMember2.MRFMember2)
		instance.empty_str = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		if not isinstance(instance.ptr_0, int):
			instance.ptr_0.arg = 0
		if not isinstance(instance.state_output_entries, int):
			instance.state_output_entries.arg = 0
		if not isinstance(instance.ptr_2, int):
			instance.ptr_2.arg = 0
		if not isinstance(instance.ptr_3, int):
			instance.ptr_3.arg = 0
		if not isinstance(instance.lua_modules, int):
			instance.lua_modules.arg = 0
		if not isinstance(instance.lua_results, int):
			instance.lua_results.arg = 0
		if not isinstance(instance.first_non_transition_state, int):
			instance.first_non_transition_state.arg = 0
		if not isinstance(instance.empty_str, int):
			instance.empty_str.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.ptr_0)
		Pointer.to_stream(stream, instance.state_output_entries)
		Pointer.to_stream(stream, instance.ptr_2)
		Pointer.to_stream(stream, instance.ptr_3)
		Uint.to_stream(stream, instance.count_0)
		Uint.to_stream(stream, instance.count_1)
		Pointer.to_stream(stream, instance.lua_modules)
		Pointer.to_stream(stream, instance.lua_results)
		Pointer.to_stream(stream, instance.first_non_transition_state)
		Pointer.to_stream(stream, instance.empty_str)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'ptr_0', Pointer, (0, generated.formats.motiongraph.compounds.MotiongraphRootFrag.MotiongraphRootFrag), (False, None)
		yield 'state_output_entries', Pointer, (0, generated.formats.motiongraph.compounds.StateArray.StateArray), (False, None)
		yield 'ptr_2', Pointer, (0, generated.formats.motiongraph.compounds.MGTwo.MGTwo), (False, None)
		yield 'ptr_3', Pointer, (0, generated.formats.motiongraph.compounds.MRFMember1.MRFMember1), (False, None)
		yield 'count_0', Uint, (0, None), (False, None)
		yield 'count_1', Uint, (0, None), (False, None)
		yield 'lua_modules', Pointer, (0, generated.formats.motiongraph.compounds.LuaModules.LuaModules), (False, None)
		yield 'lua_results', Pointer, (0, generated.formats.base.basic.ZString), (False, None)
		yield 'first_non_transition_state', Pointer, (0, generated.formats.motiongraph.compounds.MRFMember2.MRFMember2), (False, None)
		yield 'empty_str', Pointer, (0, generated.formats.base.basic.ZString), (False, None)

	def get_info_str(self, indent=0):
		return f'MotiongraphHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* ptr_0 = {self.fmt_member(self.ptr_0, indent+1)}'
		s += f'\n	* state_output_entries = {self.fmt_member(self.state_output_entries, indent+1)}'
		s += f'\n	* ptr_2 = {self.fmt_member(self.ptr_2, indent+1)}'
		s += f'\n	* ptr_3 = {self.fmt_member(self.ptr_3, indent+1)}'
		s += f'\n	* count_0 = {self.fmt_member(self.count_0, indent+1)}'
		s += f'\n	* count_1 = {self.fmt_member(self.count_1, indent+1)}'
		s += f'\n	* lua_modules = {self.fmt_member(self.lua_modules, indent+1)}'
		s += f'\n	* lua_results = {self.fmt_member(self.lua_results, indent+1)}'
		s += f'\n	* first_non_transition_state = {self.fmt_member(self.first_non_transition_state, indent+1)}'
		s += f'\n	* empty_str = {self.fmt_member(self.empty_str, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
