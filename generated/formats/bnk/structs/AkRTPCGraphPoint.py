from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class AkRTPCGraphPoint(BaseStruct):

	__name__ = 'AkRTPCGraphPoint'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.from_v = name_type_map['Float'](self.context, 0, None)
		self.to_v = name_type_map['Float'](self.context, 0, None)
		self.interp = name_type_map['Uint'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'from_v', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'to_v', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'interp', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'from_v', name_type_map['Float'], (0, None), (False, None)
		yield 'to_v', name_type_map['Float'], (0, None), (False, None)
		yield 'interp', name_type_map['Uint'], (0, None), (False, None)
