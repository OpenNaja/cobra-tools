from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ThirdFrag(MemStruct):

	"""
	72 bytes
	"""

	__name__ = 'ThirdFrag'

	_import_key = 'motiongraph.compounds.ThirdFrag'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		self.count_3 = 0
		self.count_4 = 0
		self.lua_method = Pointer(self.context, 0, ZString)
		self.ptr_1 = Pointer(self.context, 0, ThirdFrag._import_map["motiongraph.compounds.TwoPtrFirst"])
		self.ptr_2 = Pointer(self.context, 0, ThirdFrag._import_map["motiongraph.compounds.Sixtyfour"])
		self.member = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('lua_method', Pointer, (0, ZString), (False, None), None)
		yield ('count_0', Uint64, (0, None), (False, None), None)
		yield ('count_1', Uint64, (0, None), (False, None), None)
		yield ('ptr_1', Pointer, (0, ThirdFrag._import_map["motiongraph.compounds.TwoPtrFirst"]), (False, None), None)
		yield ('count_2', Uint64, (0, None), (False, None), None)
		yield ('count_3', Uint64, (0, None), (False, None), None)
		yield ('ptr_2', Pointer, (0, ThirdFrag._import_map["motiongraph.compounds.Sixtyfour"]), (False, None), None)
		yield ('count_4', Uint64, (0, None), (False, None), None)
		yield ('member', Pointer, (0, ZString), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'lua_method', Pointer, (0, ZString), (False, None)
		yield 'count_0', Uint64, (0, None), (False, None)
		yield 'count_1', Uint64, (0, None), (False, None)
		yield 'ptr_1', Pointer, (0, ThirdFrag._import_map["motiongraph.compounds.TwoPtrFirst"]), (False, None)
		yield 'count_2', Uint64, (0, None), (False, None)
		yield 'count_3', Uint64, (0, None), (False, None)
		yield 'ptr_2', Pointer, (0, ThirdFrag._import_map["motiongraph.compounds.Sixtyfour"]), (False, None)
		yield 'count_4', Uint64, (0, None), (False, None)
		yield 'member', Pointer, (0, ZString), (False, None)


ThirdFrag.init_attributes()
