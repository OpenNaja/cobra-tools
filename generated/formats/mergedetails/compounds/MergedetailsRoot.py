from generated.formats.mergedetails.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class MergedetailsRoot(MemStruct):

	"""
	48 bytes
	"""

	__name__ = 'MergedetailsRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.zero_1 = name_type_map['Uint64'](self.context, 0, None)
		self.count_0 = name_type_map['Ushort'](self.context, 0, None)
		self.count_1 = name_type_map['Ushort'](self.context, 0, None)
		self.count_2 = name_type_map['Ushort'](self.context, 0, None)
		self.count_3 = name_type_map['Ushort'](self.context, 0, None)
		self.merge_names = name_type_map['Pointer'](self.context, self.count_0, name_type_map['ZStringList'])
		self.unk_names = name_type_map['Pointer'](self.context, self.count_1, name_type_map['ZStringList'])
		self.queries = name_type_map['Pointer'](self.context, self.count_3, name_type_map['ZStringList'])
		self.field_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'merge_names', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'unk_names', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'zero_1', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'queries', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'field_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'count_0', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'count_1', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'count_2', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'count_3', name_type_map['Ushort'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'merge_names', name_type_map['Pointer'], (instance.count_0, name_type_map['ZStringList']), (False, None)
		yield 'unk_names', name_type_map['Pointer'], (instance.count_1, name_type_map['ZStringList']), (False, None)
		yield 'zero_1', name_type_map['Uint64'], (0, None), (False, None)
		yield 'queries', name_type_map['Pointer'], (instance.count_3, name_type_map['ZStringList']), (False, None)
		yield 'field_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'count_0', name_type_map['Ushort'], (0, None), (False, None)
		yield 'count_1', name_type_map['Ushort'], (0, None), (False, None)
		yield 'count_2', name_type_map['Ushort'], (0, None), (False, None)
		yield 'count_3', name_type_map['Ushort'], (0, None), (False, None)
