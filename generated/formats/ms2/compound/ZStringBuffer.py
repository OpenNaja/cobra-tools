
ZERO = b"\x00"


class ZStringBuffer:

	"""
	Holds a buffer of zero-terminated strings
	"""

	def __init__(self, arg=None, template=None):
		# arg is byte count
		self.arg = arg
		self.template = template
		self.data = b""
		self.strings = []

	def read(self, stream):
		self.data = stream.read(self.arg)
		self.strings = [x for x in self.data.split(ZERO) if x]

	def write(self, stream):
		stream.write(self.data)

	def get_str_at(self, pos):
		end = self.data.find(ZERO, pos)
		return self.data[pos:end].decode()

	def __repr__(self):
		return f"{str(self.strings)} Amount: {len(self.strings)}"

