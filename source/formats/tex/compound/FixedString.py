class FixedString:
	"""Holds a string of a fixed size, given as an argument."""

# START_CLASS

	def __init__(self, arg=None, template=None):
		# arg is byte count
		self.arg = arg
		self.template = template
		self.data = b""

	def read(self, stream):
		self.data = stream.read(self.arg)

	def write(self, stream):
		stream.write(self.data)

	def __repr__(self):
		return str(self.data)

