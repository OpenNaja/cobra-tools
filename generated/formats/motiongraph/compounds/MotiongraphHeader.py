from generated.formats.base.basic import Uint
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class MotiongraphHeader(MemStruct):

	"""
	# if self.ovl.context.version > 47:
	"""

	__name__ = 'MotiongraphHeader'

	_import_key = 'motiongraph.compounds.MotiongraphHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_0 = 0
		self.count_1 = 0
		self.ptr_0 = Pointer(self.context, 0, MotiongraphHeader._import_map["motiongraph.compounds.MotiongraphRootFrag"])
		self.state_output_entries = Pointer(self.context, 0, MotiongraphHeader._import_map["motiongraph.compounds.StateArray"])
		self.ptr_2 = Pointer(self.context, 0, MotiongraphHeader._import_map["motiongraph.compounds.MGTwo"])
		self.ptr_3 = Pointer(self.context, 0, MotiongraphHeader._import_map["motiongraph.compounds.MRFMember1"])
		self.lua_modules = Pointer(self.context, 0, MotiongraphHeader._import_map["motiongraph.compounds.LuaModules"])
		self.lua_results = Pointer(self.context, 0, ZString)
		self.first_non_transition_state = Pointer(self.context, 0, MotiongraphHeader._import_map["motiongraph.compounds.MRFMember2"])
		self.empty_str = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('ptr_0', Pointer, (0, None), (False, None), None)
		yield ('state_output_entries', Pointer, (0, None), (False, None), None)
		yield ('ptr_2', Pointer, (0, None), (False, None), None)
		yield ('ptr_3', Pointer, (0, None), (False, None), None)
		yield ('count_0', Uint, (0, None), (False, None), None)
		yield ('count_1', Uint, (0, None), (False, None), None)
		yield ('lua_modules', Pointer, (0, None), (False, None), None)
		yield ('lua_results', Pointer, (0, ZString), (False, None), None)
		yield ('first_non_transition_state', Pointer, (0, None), (False, None), None)
		yield ('empty_str', Pointer, (0, ZString), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ptr_0', Pointer, (0, MotiongraphHeader._import_map["motiongraph.compounds.MotiongraphRootFrag"]), (False, None)
		yield 'state_output_entries', Pointer, (0, MotiongraphHeader._import_map["motiongraph.compounds.StateArray"]), (False, None)
		yield 'ptr_2', Pointer, (0, MotiongraphHeader._import_map["motiongraph.compounds.MGTwo"]), (False, None)
		yield 'ptr_3', Pointer, (0, MotiongraphHeader._import_map["motiongraph.compounds.MRFMember1"]), (False, None)
		yield 'count_0', Uint, (0, None), (False, None)
		yield 'count_1', Uint, (0, None), (False, None)
		yield 'lua_modules', Pointer, (0, MotiongraphHeader._import_map["motiongraph.compounds.LuaModules"]), (False, None)
		yield 'lua_results', Pointer, (0, ZString), (False, None)
		yield 'first_non_transition_state', Pointer, (0, MotiongraphHeader._import_map["motiongraph.compounds.MRFMember2"]), (False, None)
		yield 'empty_str', Pointer, (0, ZString), (False, None)


MotiongraphHeader.init_attributes()
