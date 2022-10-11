from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class ActivityEntry(MemStruct):

	"""
	8 bytes
	"""

	__name__ = 'ActivityEntry'

	_import_key = 'motiongraph.compounds.ActivityEntry'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.value = Pointer(self.context, 0, ActivityEntry._import_map["motiongraph.compounds.Activity"])
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('value', Pointer, (0, None), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'value', Pointer, (0, ActivityEntry._import_map["motiongraph.compounds.Activity"]), (False, None)
