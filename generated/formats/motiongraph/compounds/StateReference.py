from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class StateReference(MemStruct):

	"""
	8 bytes
	"""

	__name__ = 'StateReference'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.state = name_type_map['Pointer'](self.context, 0, name_type_map['State'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'state', name_type_map['Pointer'], (0, name_type_map['State']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'state', name_type_map['Pointer'], (0, name_type_map['State']), (False, None)
