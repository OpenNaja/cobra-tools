# START_GLOBALS
from generated.formats.ovl_base.compounds.Pointer import Pointer

# END_GLOBALS


class LookupPointer(Pointer):

# START_CLASS

	def update_index(self, array):
		# check if own data has been read at same memory address as member of the array
		for i, member in enumerate(array):
			if self.data.io_start == member.io_start:
				self.pool_index = i

	def update_target(self, array):
		# set own data, then clear pool index
		self.data = array[self.pool_index]
		self.pool_index = 0

	def get_target_offset(self,):
		return self.data.io_start

	def write_ptr(self):
		"""Lookup pointer data should never be written, as it indexes into an array already written by another pointer"""
		pass
