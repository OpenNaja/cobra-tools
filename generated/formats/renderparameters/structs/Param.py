from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.renderparameters.imports import name_type_map


class Param(MemStruct):

	"""
	32 bytes
	"""

	__name__ = 'Param'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dtype = name_type_map['RenderParameterType'](self.context, 0, None)
		self.unused = name_type_map['Uint'].from_value(0)
		self.data = name_type_map['ParamData'](self.context, self.dtype, None)
		self.attribute_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'attribute_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'dtype', name_type_map['RenderParameterType'], (0, None), (False, None), (None, None)
		yield 'unused', name_type_map['Uint'], (0, None), (True, 0), (None, None)
		yield 'data', name_type_map['ParamData'], (None, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'attribute_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'dtype', name_type_map['RenderParameterType'], (0, None), (False, None)
		yield 'unused', name_type_map['Uint'], (0, None), (True, 0)
		yield 'data', name_type_map['ParamData'], (instance.dtype, None), (False, None)
