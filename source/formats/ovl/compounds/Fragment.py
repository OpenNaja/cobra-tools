# START_GLOBALS
import os

# END_GLOBALS


class Fragment:

	# START_CLASS

	@property
	def ext(self):
		return self.ext_raw.replace(":", ".")

	@ext.setter
	def ext(self, e):
		self.ext_raw = e.replace(".", ":")

	def register(self, pools):
		self.struct_ptr.add_struct(self, pools)
		target_pool = pools[self.struct_ptr.pool_index]
		self.link_ptr.add_link((target_pool, self.struct_ptr.data_offset), pools)
