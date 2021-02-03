class Matrix44:

	# START_CLASS

	def set_rows(self, mat):
		"""Set matrix from rows."""
		self.data[:] = mat
