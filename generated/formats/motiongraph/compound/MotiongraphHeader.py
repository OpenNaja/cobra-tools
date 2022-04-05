from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.motiongraph.compound.LuaModules
import generated.formats.motiongraph.compound.MGTwo
import generated.formats.motiongraph.compound.MRFMember1
import generated.formats.motiongraph.compound.MRFMember2
import generated.formats.motiongraph.compound.MotiongraphRootFrag
import generated.formats.motiongraph.compound.StateArray
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class MotiongraphHeader(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.count_0 = 0
		self.count_1 = 0
		self.ptr_0 = Pointer(self.context, 0, generated.formats.motiongraph.compound.MotiongraphRootFrag.MotiongraphRootFrag)
		self.state_output_entries = Pointer(self.context, 0, generated.formats.motiongraph.compound.StateArray.StateArray)
		self.ptr_2 = Pointer(self.context, 0, generated.formats.motiongraph.compound.MGTwo.MGTwo)
		self.ptr_3 = Pointer(self.context, 0, generated.formats.motiongraph.compound.MRFMember1.MRFMember1)
		self.lua_modules = Pointer(self.context, 0, generated.formats.motiongraph.compound.LuaModules.LuaModules)
		self.lua_results = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.first_non_transition_state = Pointer(self.context, 0, generated.formats.motiongraph.compound.MRFMember2.MRFMember2)
		self.empty_str = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.count_0 = 0
		self.count_1 = 0
		self.ptr_0 = Pointer(self.context, 0, generated.formats.motiongraph.compound.MotiongraphRootFrag.MotiongraphRootFrag)
		self.state_output_entries = Pointer(self.context, 0, generated.formats.motiongraph.compound.StateArray.StateArray)
		self.ptr_2 = Pointer(self.context, 0, generated.formats.motiongraph.compound.MGTwo.MGTwo)
		self.ptr_3 = Pointer(self.context, 0, generated.formats.motiongraph.compound.MRFMember1.MRFMember1)
		self.lua_modules = Pointer(self.context, 0, generated.formats.motiongraph.compound.LuaModules.LuaModules)
		self.lua_results = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.first_non_transition_state = Pointer(self.context, 0, generated.formats.motiongraph.compound.MRFMember2.MRFMember2)
		self.empty_str = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.ptr_0 = Pointer.from_stream(stream, instance.context, 0, generated.formats.motiongraph.compound.MotiongraphRootFrag.MotiongraphRootFrag)
		instance.state_output_entries = Pointer.from_stream(stream, instance.context, 0, generated.formats.motiongraph.compound.StateArray.StateArray)
		instance.ptr_2 = Pointer.from_stream(stream, instance.context, 0, generated.formats.motiongraph.compound.MGTwo.MGTwo)
		instance.ptr_3 = Pointer.from_stream(stream, instance.context, 0, generated.formats.motiongraph.compound.MRFMember1.MRFMember1)
		instance.count_0 = stream.read_uint()
		instance.count_1 = stream.read_uint()
		instance.lua_modules = Pointer.from_stream(stream, instance.context, 0, generated.formats.motiongraph.compound.LuaModules.LuaModules)
		instance.lua_results = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.first_non_transition_state = Pointer.from_stream(stream, instance.context, 0, generated.formats.motiongraph.compound.MRFMember2.MRFMember2)
		instance.empty_str = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.ptr_0.arg = 0
		instance.state_output_entries.arg = 0
		instance.ptr_2.arg = 0
		instance.ptr_3.arg = 0
		instance.lua_modules.arg = 0
		instance.lua_results.arg = 0
		instance.first_non_transition_state.arg = 0
		instance.empty_str.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.ptr_0)
		Pointer.to_stream(stream, instance.state_output_entries)
		Pointer.to_stream(stream, instance.ptr_2)
		Pointer.to_stream(stream, instance.ptr_3)
		stream.write_uint(instance.count_0)
		stream.write_uint(instance.count_1)
		Pointer.to_stream(stream, instance.lua_modules)
		Pointer.to_stream(stream, instance.lua_results)
		Pointer.to_stream(stream, instance.first_non_transition_state)
		Pointer.to_stream(stream, instance.empty_str)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'MotiongraphHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* ptr_0 = {fmt_member(self.ptr_0, indent+1)}'
		s += f'\n	* state_output_entries = {fmt_member(self.state_output_entries, indent+1)}'
		s += f'\n	* ptr_2 = {fmt_member(self.ptr_2, indent+1)}'
		s += f'\n	* ptr_3 = {fmt_member(self.ptr_3, indent+1)}'
		s += f'\n	* count_0 = {fmt_member(self.count_0, indent+1)}'
		s += f'\n	* count_1 = {fmt_member(self.count_1, indent+1)}'
		s += f'\n	* lua_modules = {fmt_member(self.lua_modules, indent+1)}'
		s += f'\n	* lua_results = {fmt_member(self.lua_results, indent+1)}'
		s += f'\n	* first_non_transition_state = {fmt_member(self.first_non_transition_state, indent+1)}'
		s += f'\n	* empty_str = {fmt_member(self.empty_str, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
