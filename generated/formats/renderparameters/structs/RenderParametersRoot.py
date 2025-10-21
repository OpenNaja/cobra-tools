from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.renderparameters.imports import name_type_map


class RenderParametersRoot(MemStruct):

	"""
	32 bytes
	"""

	__name__ = 'RenderParametersRoot'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.params_count = name_type_map['Uint64'](self.context, 0, None)
		self.unk = name_type_map['Uint64'](self.context, 0, None)
		self.param_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZStringObfuscated'])
		self.params = name_type_map['Pointer'](self.context, self.params_count, name_type_map['ParamList'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'param_name', name_type_map['Pointer'], (0, name_type_map['ZStringObfuscated']), (False, None), (None, None)
		yield 'params', name_type_map['Pointer'], (None, name_type_map['ParamList']), (False, None), (None, None)
		yield 'params_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)
		yield 'unk', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'param_name', name_type_map['Pointer'], (0, name_type_map['ZStringObfuscated']), (False, None)
		yield 'params', name_type_map['Pointer'], (instance.params_count, name_type_map['ParamList']), (False, None)
		yield 'params_count', name_type_map['Uint64'], (0, None), (False, None)
		yield 'unk', name_type_map['Uint64'], (0, None), (False, None)
