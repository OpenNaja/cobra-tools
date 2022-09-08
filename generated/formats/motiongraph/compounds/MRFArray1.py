from generated.array import Array
from generated.formats.motiongraph.compounds.MRFEntry1 import MRFEntry1
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class MRFArray1(MemStruct):

	__name__ = 'MRFArray1'

	_import_path = 'generated.formats.motiongraph.compounds.MRFArray1'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.states = Array(self.context, 0, None, (0,), MRFEntry1)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.states = Array(self.context, 0, None, (self.arg,), MRFEntry1)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'states', Array, (0, None, (instance.arg,), MRFEntry1), (False, None)

	def get_info_str(self, indent=0):
		return f'MRFArray1 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
