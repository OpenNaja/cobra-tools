from generated.array import Array
from generated.formats.motiongraph.compounds.ActivitiesLink import ActivitiesLink
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class ActivitiesLinks(MemStruct):

	__name__ = 'ActivitiesLinks'

	_import_key = 'motiongraph.compounds.ActivitiesLinks'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.activities = Array(self.context, 0, None, (0,), ActivitiesLink)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('activities', Array, (0, None, (None,), ActivitiesLink), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'activities', Array, (0, None, (instance.arg,), ActivitiesLink), (False, None)
