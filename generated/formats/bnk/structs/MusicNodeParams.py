from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class MusicNodeParams(BaseStruct):

	__name__ = 'MusicNodeParams'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_flags = name_type_map['Ubyte'](self.context, 0, None)
		self.node_base_params = name_type_map['NodeBaseParams'](self.context, 0, None)
		self.ul_num_childs = name_type_map['Uint'](self.context, 0, None)
		self.children = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.ak_meter_info = name_type_map['AkMeterInfo'](self.context, 0, None)
		self.b_meter_info_flag = name_type_map['Ubyte'](self.context, 0, None)
		self.num_stingers = name_type_map['Uint'](self.context, 0, None)
		self.stingers = Array(self.context, 0, None, (0,), name_type_map['CAkStinger'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'u_flags', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'node_base_params', name_type_map['NodeBaseParams'], (0, None), (False, None), (None, None)
		yield 'ul_num_childs', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'children', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)
		yield 'ak_meter_info', name_type_map['AkMeterInfo'], (0, None), (False, None), (None, None)
		yield 'b_meter_info_flag', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'num_stingers', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'stingers', Array, (0, None, (None,), name_type_map['CAkStinger']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'u_flags', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'node_base_params', name_type_map['NodeBaseParams'], (0, None), (False, None)
		yield 'ul_num_childs', name_type_map['Uint'], (0, None), (False, None)
		yield 'children', Array, (0, None, (instance.ul_num_childs,), name_type_map['Uint']), (False, None)
		yield 'ak_meter_info', name_type_map['AkMeterInfo'], (0, None), (False, None)
		yield 'b_meter_info_flag', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'num_stingers', name_type_map['Uint'], (0, None), (False, None)
		yield 'stingers', Array, (0, None, (instance.num_stingers,), name_type_map['CAkStinger']), (False, None)
