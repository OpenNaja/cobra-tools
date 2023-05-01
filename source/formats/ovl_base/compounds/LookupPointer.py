# START_GLOBALS
from generated.formats.ovl_base.compounds.Pointer import Pointer

# END_GLOBALS


class LookupPointer(Pointer):

# START_CLASS

	def update_index(self, array):
		# check if own data has been read at same memory address as member of the array
		for i, member in enumerate(array):
			if self._data.io_start == member.io_start:
				self.pool_index = i

	def update_data(self, array):
		# set own data, then clear pool index
		self._data = array[self.pool_index]
		self.pool_index = 0
