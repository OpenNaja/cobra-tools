from generated.formats.ovl_base.compounds.Pointer import Pointer

from generated.formats.ovl_base.compounds.Pointer import Pointer


class LookupPointer(Pointer):

	__name__ = 'LookupPointer'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	def update_index(self, array):
		# check if own data has been read at same memory address as member of the array
		for i, member in enumerate(array):
			if self.data.io_start == member.io_start:
				self.pool_index = i

	def update_data(self, array):
		# set own data, then clear pool index
		self.data = array[self.pool_index]
		self.pool_index = 0

