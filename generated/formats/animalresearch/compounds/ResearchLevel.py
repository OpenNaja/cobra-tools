from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ResearchLevel(MemStruct):

	__name__ = 'ResearchLevel'

	_import_key = 'animalresearch.compounds.ResearchLevel'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.next_level_count = 0
		self.children_count = 0
		self.level_name = Pointer(self.context, 0, ZString)
		self.next_levels = Pointer(self.context, self.next_level_count, ResearchLevel._import_map["animalresearch.compounds.PtrList"])
		self.children = Pointer(self.context, self.children_count, ResearchLevel._import_map["animalresearch.compounds.PtrList"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('level_name', Pointer, (0, ZString), (False, None), (None, None))
		yield ('next_levels', Pointer, (None, ResearchLevel._import_map["animalresearch.compounds.PtrList"]), (False, None), (None, None))
		yield ('next_level_count', Uint64, (0, None), (False, None), (None, None))
		yield ('children', Pointer, (None, ResearchLevel._import_map["animalresearch.compounds.PtrList"]), (False, None), (None, None))
		yield ('children_count', Uint64, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'level_name', Pointer, (0, ZString), (False, None)
		yield 'next_levels', Pointer, (instance.next_level_count, ResearchLevel._import_map["animalresearch.compounds.PtrList"]), (False, None)
		yield 'next_level_count', Uint64, (0, None), (False, None)
		yield 'children', Pointer, (instance.children_count, ResearchLevel._import_map["animalresearch.compounds.PtrList"]), (False, None)
		yield 'children_count', Uint64, (0, None), (False, None)
