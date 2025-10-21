from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.trackstation.imports import name_type_map


class FlumeInfo(MemStruct):

	__name__ = 'FlumeInfo'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.starts_count = name_type_map['Uint64'](self.context, 0, None)
		self.ends_count = name_type_map['Uint64'](self.context, 0, None)
		self.starts = name_type_map['ArrayPointer'](self.context, self.starts_count, name_type_map['Start'])
		self.ends = name_type_map['ArrayPointer'](self.context, self.ends_count, name_type_map['End'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'starts', name_type_map['ArrayPointer'], (None, name_type_map['Start']), (False, None), (None, None)
		yield 'starts_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'ends', name_type_map['ArrayPointer'], (None, name_type_map['End']), (False, None), (None, None)
		yield 'ends_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'starts', name_type_map['ArrayPointer'], (instance.starts_count, name_type_map['Start']), (False, None)
		yield 'starts_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'ends', name_type_map['ArrayPointer'], (instance.ends_count, name_type_map['End']), (False, None)
		yield 'ends_count', name_type_map['Uint64'], (0, None), (False, None)
