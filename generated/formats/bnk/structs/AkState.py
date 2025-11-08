from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class AkState(BaseStruct):

	__name__ = 'AkState'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ul_state_i_d = name_type_map['Uint'](self.context, 0, None)
		self.ul_state_instance_i_d = name_type_map['Uint'](self.context, 0, None)
		self.n_props = name_type_map['Ushort'](self.context, 0, None)
		self.p_props = Array(self.context, 0, None, (0,), name_type_map['AkPropBundleUshortFloat'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'ul_state_i_d', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'ul_state_instance_i_d', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version <= 145, None)
		yield 'n_props', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version >= 146, None)
		yield 'p_props', Array, (0, None, (None,), name_type_map['AkPropBundleUshortFloat']), (False, None), (lambda context: context.version >= 146, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ul_state_i_d', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version <= 145:
			yield 'ul_state_instance_i_d', name_type_map['Uint'], (0, None), (False, None)
		if instance.context.version >= 146:
			yield 'n_props', name_type_map['Ushort'], (0, None), (False, None)
			yield 'p_props', Array, (0, None, (instance.n_props,), name_type_map['AkPropBundleUshortFloat']), (False, None)
