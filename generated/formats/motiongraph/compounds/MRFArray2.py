from generated.array import Array
from generated.formats.motiongraph.compounds.MRFEntry2 import MRFEntry2
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class MRFArray2(MemStruct):

	__name__ = 'MRFArray2'

	_import_key = 'motiongraph.compounds.MRFArray2'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.states = Array(self.context, 0, None, (0,), MRFEntry2)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'states', Array, (0, None, (instance.arg,), MRFEntry2), (False, None)
