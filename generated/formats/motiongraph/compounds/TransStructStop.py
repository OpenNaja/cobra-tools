from generated.formats.motiongraph.compounds.MGTwo import MGTwo
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TransStructStop(MemStruct):

	"""
	24 bytes
	actually same as above, just don't keep reading here
	"""

	__name__ = 'TransStructStop'

	_import_key = 'motiongraph.compounds.TransStructStop'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.other_states = MGTwo(self.context, 0, None)
		self.another_mrfentry_2 = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('another_mrfentry_2', Pointer, (0, None), (False, None), None)
		yield ('other_states', MGTwo, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'another_mrfentry_2', Pointer, (0, None), (False, None)
		yield 'other_states', MGTwo, (0, None), (False, None)


TransStructStop.init_attributes()
