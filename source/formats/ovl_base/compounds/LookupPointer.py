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

	def update_target(self, array_ptr):
		# set own data, then clear pool index
		self.data = array_ptr.data[self.pool_index]
		self.array_ptr = array_ptr
		self.pool_index = 0

	def write_ptr(self, loader, src_pool):
		"""Lookup pointer data should never be written, as it indexes into an array already written by another pointer"""
		loader.attach_frag_to_ptr(src_pool, self.io_start, self.array_ptr.target_pool, self.data.io_start)
