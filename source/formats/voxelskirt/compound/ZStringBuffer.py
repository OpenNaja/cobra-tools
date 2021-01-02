# START_GLOBALS
ZERO = b"\x00"


# END_GLOBALS

class ZStringBuffer:
	"""Holds a buffer of zero-terminated strings"""

# START_CLASS

	def __init__(self, arg=None, template=None):
		# arg is byte count
		self.arg = arg
		self.template = template
		self.data = b""
		self.strings = []

	def read(self, stream):
		self.data = stream.read(self.arg)
		self.strings = self.data.split(ZERO)

	def write(self, stream):
		stream.write(self.data)

	def get_str_at(self, pos):
		end = self.data.find(ZERO, pos)
		return self.data[pos:end].decode()

	def __repr__(self):
		return str(self.strings)
