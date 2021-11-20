from generated.context import ContextReference


class FixedString:

	"""
	The string "DDS ".
	"""

	context = ContextReference()

	def set_defaults(self):
		pass

	def __init__(self, context, arg=0, template=None):
		self.name = ''
		self._context = context
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


