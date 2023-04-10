from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.path.imports import name_type_map


class Connector(MemStruct):

	__name__ = 'Connector'

	_import_key = 'path.compounds.Connector'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.unk_vector = name_type_map['Vector2'](self.context, 0, None)
		self.model_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.joint_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('model_name', name_type_map['Pointer'], (0, None), (False, None), (None, None))
		yield ('joint_name', name_type_map['Pointer'], (0, None), (False, None), (None, None))
		yield ('unk_vector', name_type_map['Vector2'], (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'model_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'joint_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'unk_vector', name_type_map['Vector2'], (0, None), (False, None)
