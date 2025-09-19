from generated.array import Array
from generated.formats.bnk.compounds.HircObject import HircObject
from generated.formats.bnk.imports import name_type_map


class Event(HircObject):

	__name__ = 'Event'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.num_actions = name_type_map['Ubyte'](self.context, 0, None)
		self.children = Array(self.context, 0, None, (0,), name_type_map['Uint'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'num_actions', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'children', Array, (0, None, (None,), name_type_map['Uint']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'num_actions', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'children', Array, (0, None, (instance.num_actions,), name_type_map['Uint']), (False, None)
