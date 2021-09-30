
from generated.io import MAX_LEN

ZERO = b"\x00"


from generated.context import ContextReference


class SmartPadding:

	"""
	Grabs 00 bytes only
	"""

	context = ContextReference()

	def __init__(self, arg=None, template=None):
		# arg is byte count
		self.arg = arg
		self.template = template
		self.data = b""

	def read(self, stream):
		self.data = b''
		for i in range(MAX_LEN):
			end = stream.tell()
			char = stream.read(1)
			# stop if a byte other than 00 is encountered
			if char != ZERO:
				break
			# it's 00 so add it to the padding
			self.data += char
		else:
			raise ValueError('padding too long')
		stream.seek(end)

	def write(self, stream):
		stream.write(self.data)

	def __repr__(self):
		return f"{self.data} Size: {len(self.data)}"

