from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.structs.MemStruct import MemStruct


class MrfReference2(MemStruct):

	"""
	8 bytes
	"""

	__name__ = 'MRF_Reference2'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.value = name_type_map['Pointer'](self.context, 0, name_type_map['MRFMember2'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'value', name_type_map['Pointer'], (0, name_type_map['MRFMember2']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'value', name_type_map['Pointer'], (0, name_type_map['MRFMember2']), (False, None)
