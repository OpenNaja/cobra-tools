from generated.formats.motiongraph.imports import name_type_map
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ActivityReference(MemStruct):

	"""
	8 bytes
	"""

	__name__ = 'ActivityReference'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.activity = name_type_map['Pointer'](self.context, 0, name_type_map['Activity'])
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'activity', name_type_map['Pointer'], (0, name_type_map['Activity']), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'activity', name_type_map['Pointer'], (0, name_type_map['Activity']), (False, None)
