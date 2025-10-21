from generated.formats.chapterdata.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class ChapterDataRoot(MemStruct):

	__name__ = 'ChapterDataRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.chapter_data_type = name_type_map['Ubyte'](self.context, 0, None)
		self.chapter_data_hidden = name_type_map['Ubyte'](self.context, 0, None)
		self.chapter_data_id = name_type_map['Ubyte'](self.context, 0, None)
		self.chapter_data_zero = name_type_map['Ubyte'](self.context, 0, None)
		self.chapter_data_unused_1 = name_type_map['Uint'](self.context, 0, None)
		self.chapter_data_list_1 = name_type_map['Uint64'](self.context, 0, None)
		self.chapter_data_list_2 = name_type_map['Uint64'](self.context, 0, None)
		self.chapter_data_list_3 = name_type_map['Uint64'](self.context, 0, None)
		self.chapter_data_list_4 = name_type_map['Uint64'](self.context, 0, None)
		self.chapter_data_count_1 = name_type_map['Uint'](self.context, 0, None)
		self.chapter_data_count_2 = name_type_map['Uint'](self.context, 0, None)
		self.chapter_data_count_3 = name_type_map['Uint'](self.context, 0, None)
		self.chapter_data_count_4 = name_type_map['Uint'](self.context, 0, None)
		self.chapter_data_count = name_type_map['Uint64'](self.context, 0, None)
		self.chapter_data_unused_2 = name_type_map['Uint64'](self.context, 0, None)
		self.chapter_data_list = name_type_map['ArrayPointer'](self.context, self.chapter_data_count, name_type_map['ChapterData'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'chapter_data_type', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'chapter_data_hidden', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'chapter_data_id', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'chapter_data_zero', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'chapter_data_unused_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'chapter_data_list_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'chapter_data_list_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'chapter_data_list_3', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'chapter_data_list_4', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'chapter_data_count_1', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'chapter_data_count_2', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'chapter_data_count_3', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'chapter_data_count_4', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'chapter_data_list', name_type_map['ArrayPointer'], (None, name_type_map['ChapterData']), (False, None), (None, None)
		yield 'chapter_data_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'chapter_data_unused_2', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'chapter_data_type', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'chapter_data_hidden', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'chapter_data_id', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'chapter_data_zero', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'chapter_data_unused_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'chapter_data_list_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'chapter_data_list_2', name_type_map['Uint64'], (0, None), (False, None)
		yield 'chapter_data_list_3', name_type_map['Uint64'], (0, None), (False, None)
		yield 'chapter_data_list_4', name_type_map['Uint64'], (0, None), (False, None)
		yield 'chapter_data_count_1', name_type_map['Uint'], (0, None), (False, None)
		yield 'chapter_data_count_2', name_type_map['Uint'], (0, None), (False, None)
		yield 'chapter_data_count_3', name_type_map['Uint'], (0, None), (False, None)
		yield 'chapter_data_count_4', name_type_map['Uint'], (0, None), (False, None)
		yield 'chapter_data_list', name_type_map['ArrayPointer'], (instance.chapter_data_count, name_type_map['ChapterData']), (False, None)
		yield 'chapter_data_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'chapter_data_unused_2', name_type_map['Uint64'], (0, None), (False, None)
