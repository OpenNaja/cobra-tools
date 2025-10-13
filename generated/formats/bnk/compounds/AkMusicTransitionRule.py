from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class AkMusicTransitionRule(BaseStruct):

	__name__ = 'AkMusicTransitionRule'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_num_src = name_type_map['Uint'](self.context, 0, None)
		self.src_i_d = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.u_num_dst = name_type_map['Uint'](self.context, 0, None)
		self.dst_i_d = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		self.src_rule = name_type_map['AkMusicTransSrcRule'](self.context, 0, None)
		self.dst_rule = name_type_map['AkMusicTransDstRule'](self.context, 0, None)
		self.alloc_trans_object_flag = name_type_map['Ubyte'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'u_num_src', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'src_i_d', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)
		yield 'u_num_dst', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'dst_i_d', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)
		yield 'src_rule', name_type_map['AkMusicTransSrcRule'], (0, None), (False, None), (None, None)
		yield 'dst_rule', name_type_map['AkMusicTransDstRule'], (0, None), (False, None), (None, None)
		yield 'alloc_trans_object_flag', name_type_map['Ubyte'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'u_num_src', name_type_map['Uint'], (0, None), (False, None)
		yield 'src_i_d', Array, (0, None, (instance.u_num_src,), name_type_map['Uint']), (False, None)
		yield 'u_num_dst', name_type_map['Uint'], (0, None), (False, None)
		yield 'dst_i_d', Array, (0, None, (instance.u_num_dst,), name_type_map['Uint']), (False, None)
		yield 'src_rule', name_type_map['AkMusicTransSrcRule'], (0, None), (False, None)
		yield 'dst_rule', name_type_map['AkMusicTransDstRule'], (0, None), (False, None)
		yield 'alloc_trans_object_flag', name_type_map['Ubyte'], (0, None), (False, None)
