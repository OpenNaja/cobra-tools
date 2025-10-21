from generated.formats.ovl_base.structs.MemStruct import MemStruct
from generated.formats.renderparameters.imports import name_type_map


class CurveParam(MemStruct):

	__name__ = 'CurveParam'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.dtype = name_type_map['RenderParameterType'](self.context, 0, None)

		# set to 1 if count > 1
		self.do_interpolation = name_type_map['Uint'](self.context, 0, None)
		self.samples_count = name_type_map['Uint64'](self.context, 0, None)
		self.attribute_name = name_type_map['Pointer'](self.context, 0, name_type_map['ZString'])
		self.samples = name_type_map['Pointer'](self.context, (self.samples_count, self.dtype), name_type_map['CurveList'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'attribute_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None), (None, None)
		yield 'dtype', name_type_map['RenderParameterType'], (0, None), (False, None), (None, None)
		yield 'do_interpolation', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'samples', name_type_map['Pointer'], (None, name_type_map['CurveList']), (False, None), (None, None)
		yield 'samples_count', name_type_map['Uint64'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'attribute_name', name_type_map['Pointer'], (0, name_type_map['ZString']), (False, None)
		yield 'dtype', name_type_map['RenderParameterType'], (0, None), (False, None)
		yield 'do_interpolation', name_type_map['Uint'], (0, None), (False, None)
		yield 'samples', name_type_map['Pointer'], ((instance.samples_count, instance.dtype), name_type_map['CurveList']), (False, None)
		yield 'samples_count', name_type_map['Uint64'], (0, None), (False, None)
