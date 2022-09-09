from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ResearchLevel(MemStruct):

	__name__ = 'ResearchLevel'

	_import_path = 'generated.formats.animalresearch.compounds.ResearchLevel'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.next_level_count = 0
		self.children_count = 0
		self.level_name = Pointer(self.context, 0, ZString)
		self.next_levels = Pointer(self.context, self.next_level_count, ResearchLevel._import_path_map["generated.formats.animalresearch.compounds.PtrList"])
		self.children = Pointer(self.context, self.children_count, ResearchLevel._import_path_map["generated.formats.animalresearch.compounds.PtrList"])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'level_name', Pointer, (0, ZString), (False, None)
		yield 'next_levels', Pointer, (instance.next_level_count, ResearchLevel._import_path_map["generated.formats.animalresearch.compounds.PtrList"]), (False, None)
		yield 'next_level_count', Uint64, (0, None), (False, None)
		yield 'children', Pointer, (instance.children_count, ResearchLevel._import_path_map["generated.formats.animalresearch.compounds.PtrList"]), (False, None)
		yield 'children_count', Uint64, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'ResearchLevel [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
