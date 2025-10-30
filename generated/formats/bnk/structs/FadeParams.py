from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class FadeParams(BaseStruct):

	__name__ = 'fadeParams'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.transition_time = name_type_map['Int'](self.context, 0, None)
		self.e_fade_curve = name_type_map['Uint'](self.context, 0, None)
		self.i_fade_offset = name_type_map['Int'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'transition_time', name_type_map['Int'], (0, None), (False, None), (None, None)
		yield 'e_fade_curve', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'i_fade_offset', name_type_map['Int'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'transition_time', name_type_map['Int'], (0, None), (False, None)
		yield 'e_fade_curve', name_type_map['Uint'], (0, None), (False, None)
		yield 'i_fade_offset', name_type_map['Int'], (0, None), (False, None)
