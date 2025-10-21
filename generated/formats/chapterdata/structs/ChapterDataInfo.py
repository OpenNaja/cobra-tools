from generated.formats.chapterdata.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ChapterDataInfo(MemStruct):

	__name__ = 'ChapterDataInfo'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.chapter_data_into_str_1 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.chapter_data_into_str_2 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.chapter_data_into_str_3 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.chapter_data_into_str_4 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.chapter_data_into_str_5 = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'chapter_data_into_str_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'chapter_data_into_str_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'chapter_data_into_str_3', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'chapter_data_into_str_4', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'chapter_data_into_str_5', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'chapter_data_into_str_1', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'chapter_data_into_str_2', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'chapter_data_into_str_3', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'chapter_data_into_str_4', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'chapter_data_into_str_5', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
