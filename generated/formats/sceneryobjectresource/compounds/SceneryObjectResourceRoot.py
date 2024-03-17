from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.sceneryobjectresource.imports import name_type_map


class SceneryObjectResourceRoot(MemStruct):

	__name__ = 'SceneryObjectResourceRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data_1_count = name_type_map['Uint64'](self.context, 0, None)
		self.data_2_count = name_type_map['Uint64'](self.context, 0, None)
		self.data_3_count = name_type_map['Uint64'](self.context, 0, None)
		self.data_4_count = name_type_map['Uint64'](self.context, 0, None)
		self.data_1 = name_type_map['Pointer'](self.context, self.data_1_count, name_type_map['ZStringList'])
		self.data_2 = name_type_map['Pointer'](self.context, self.data_2_count, name_type_map['ZStringList'])
		self.data_3 = name_type_map['Pointer'](self.context, self.data_3_count, name_type_map['ZStringList'])
		self.data_4 = name_type_map['Pointer'](self.context, self.data_4_count, name_type_map['ZStringList'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'data_1', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'data_1_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'data_2', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'data_2_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'data_3', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'data_3_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'data_4', name_type_map['Pointer'], (None, name_type_map['ZStringList']), (False, None), (None, None)
		yield 'data_4_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'data_1', name_type_map['Pointer'], (instance.data_1_count, name_type_map['ZStringList']), (False, None)
		yield 'data_1_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'data_2', name_type_map['Pointer'], (instance.data_2_count, name_type_map['ZStringList']), (False, None)
		yield 'data_2_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'data_3', name_type_map['Pointer'], (instance.data_3_count, name_type_map['ZStringList']), (False, None)
		yield 'data_3_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'data_4', name_type_map['Pointer'], (instance.data_4_count, name_type_map['ZStringList']), (False, None)
		yield 'data_4_count', name_type_map['Uint64'], (0, None), (False, None)
