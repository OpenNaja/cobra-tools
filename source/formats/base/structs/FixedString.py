class FixedString:
	"""Holds a string of a fixed size, given as an argument."""

# START_CLASS

	@classmethod
	def format_indented(cls, self, indent=0):
		return str(self.data)
