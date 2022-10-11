from generated.array import Array
from generated.formats.motiongraph.compounds.ActivityEntry import ActivityEntry
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Activities(MemStruct):

	__name__ = 'Activities'

	_import_key = 'motiongraph.compounds.Activities'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.states = Array(self.context, 0, None, (0,), ActivityEntry)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('states', Array, (0, None, (None,), ActivityEntry), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'states', Array, (0, None, (instance.arg,), ActivityEntry), (False, None)
