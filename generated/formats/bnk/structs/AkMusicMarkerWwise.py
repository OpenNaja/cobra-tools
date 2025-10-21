from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class AkMusicMarkerWwise(BaseStruct):

	__name__ = 'AkMusicMarkerWwise'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.id = name_type_map['Uint'](self.context, 0, None)
		self.f_position = name_type_map['Double'](self.context, 0, None)
		self.p_marker_name = name_type_map['ZString'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'id', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'f_position', name_type_map['Double'], (0, None), (False, None), (None, None)
		yield 'p_marker_name', name_type_map['ZString'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'id', name_type_map['Uint'], (0, None), (False, None)
		yield 'f_position', name_type_map['Double'], (0, None), (False, None)
		yield 'p_marker_name', name_type_map['ZString'], (0, None), (False, None)
