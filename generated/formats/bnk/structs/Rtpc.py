from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class Rtpc(BaseStruct):

	__name__ = 'RTPC'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.rtpcid = name_type_map['Uint'](self.context, 0, None)
		self.rtpc_type = name_type_map['Ubyte'](self.context, 0, None)
		self.rtpc_accum = name_type_map['Ubyte'](self.context, 0, None)
		self.param_i_d = name_type_map['Ubyte'](self.context, 0, None)
		self.rtpc_curve_i_d = name_type_map['Uint'](self.context, 0, None)
		self.e_scaling = name_type_map['Ubyte'](self.context, 0, None)
		self.ul_size = name_type_map['Ushort'](self.context, 0, None)
		self.graph = Array(self.context, 0, None, (0,), name_type_map['AkRTPCGraphPoint'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'rtpcid', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'rtpc_type', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'rtpc_accum', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'param_i_d', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'rtpc_curve_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'e_scaling', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'ul_size', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'graph', Array, (0, None, (None,), name_type_map['AkRTPCGraphPoint']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'rtpcid', name_type_map['Uint'], (0, None), (False, None)
		yield 'rtpc_type', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'rtpc_accum', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'param_i_d', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'rtpc_curve_i_d', name_type_map['Uint'], (0, None), (False, None)
		yield 'e_scaling', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'ul_size', name_type_map['Ushort'], (0, None), (False, None)
		yield 'graph', Array, (0, None, (instance.ul_size,), name_type_map['AkRTPCGraphPoint']), (False, None)
