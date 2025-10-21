class FileEntry:

	# START_CLASS

	def update_constants(self, ovl):
		"""Update the constants"""
		self.pool_type = ovl.get_mime(self.ext, "pool")
		self.set_pool_type = ovl.get_mime(self.ext, "set_pool")
