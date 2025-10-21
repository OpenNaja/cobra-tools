from generated.formats.codexdata.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class CodexDataRoot(MemStruct):

	__name__ = 'CodexDataRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.codex_data_count = name_type_map['Uint64'](self.context, 0, None)
		self.codex_data_list = name_type_map['ArrayPointer'](self.context, self.codex_data_count, name_type_map['CodexChapter'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'codex_data_list', name_type_map['ArrayPointer'], (None, name_type_map['CodexChapter']), (False, None), (None, None)
		yield 'codex_data_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'codex_data_list', name_type_map['ArrayPointer'], (instance.codex_data_count, name_type_map['CodexChapter']), (False, None)
		yield 'codex_data_count', name_type_map['Uint64'], (0, None), (False, None)
