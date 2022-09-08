from generated.formats.motiongraph.compounds.StateArray import StateArray
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class TransStruct(MemStruct):

	"""
	24 bytes
	"""

	__name__ = 'TransStruct'

	_import_path = 'generated.formats.motiongraph.compounds.TransStruct'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.states = StateArray(self.context, 0, None)
		self.another_mrfentry_2 = Pointer(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'another_mrfentry_2', Pointer, (0, None), (False, None)
		yield 'states', StateArray, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'TransStruct [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
