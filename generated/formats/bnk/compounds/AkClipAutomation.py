from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class AkClipAutomation(BaseStruct):

	__name__ = 'AkClipAutomation'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_clip_index = name_type_map['Uint'](self.context, 0, None)
		self.e_auto_type = name_type_map['Uint'](self.context, 0, None)
		self.u_num_points = name_type_map['Uint'](self.context, 0, None)
		self.graph = Array(self.context, 0, None, (0,), name_type_map['AkRTPCGraphPoint'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'u_clip_index', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'e_auto_type', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'u_num_points', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'graph', Array, (0, None, (None,), name_type_map['AkRTPCGraphPoint']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'u_clip_index', name_type_map['Uint'], (0, None), (False, None)
		yield 'e_auto_type', name_type_map['Uint'], (0, None), (False, None)
		yield 'u_num_points', name_type_map['Uint'], (0, None), (False, None)
		yield 'graph', Array, (0, None, (instance.u_num_points,), name_type_map['AkRTPCGraphPoint']), (False, None)
