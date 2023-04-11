from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.path.imports import name_type_map


class PathExtrusion(MemStruct):

	__name__ = 'PathExtrusion'

	_import_key = 'path.compounds.PathExtrusion'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_float_1 = name_type_map['Float'](self.context, 0, None)
		self.unk_float_2 = name_type_map['Float'](self.context, 0, None)
		self.is_kerb = name_type_map['Bool'](self.context, 0, None)
		self.is_not_ground = name_type_map['Bool'].from_value(True)
		self.model = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.post_model = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.endcap_model = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None))
		yield ('post_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None))
		yield ('endcap_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None))
		yield ('unk_float_1', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('unk_float_2', name_type_map['Float'], (0, None), (False, None), (None, None))
		yield ('is_kerb', name_type_map['Bool'], (0, None), (False, None), (None, None))
		yield ('is_not_ground', name_type_map['Bool'], (0, None), (False, True), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'post_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'endcap_model', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_float_1', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_float_2', name_type_map['Float'], (0, None), (False, None)
		yield 'is_kerb', name_type_map['Bool'], (0, None), (False, None)
		yield 'is_not_ground', name_type_map['Bool'], (0, None), (False, True)
