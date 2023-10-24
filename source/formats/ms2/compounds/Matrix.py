class Matrix:

	# START_CLASS

	def set_rows(self, mat):
		"""Set matrix from rows."""
		self.data[:] = mat.transposed()
