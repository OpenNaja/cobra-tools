from generated.base_struct import BaseStruct
from generated.formats.bnk.imports import name_type_map


class HircObject(BaseStruct):

	__name__ = 'HircObject'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# length of this section
		self.length = name_type_map['Uint'](self.context, 0, None)

		# id of this Sound SFX object
		self.id = name_type_map['Uint'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'length', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'id', name_type_map['Uint'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'length', name_type_map['Uint'], (0, None), (False, None)
		yield 'id', name_type_map['Uint'], (0, None), (False, None)
