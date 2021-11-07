# START_GLOBALS
from generated.io import MAX_LEN
from modules.formats.shared import get_padding_size

ZERO = b"\x00"


# END_GLOBALS


from generated.context import ContextReference


class PadAlign:
	"""Automatically aligns to arg's start and pads so aligned with align"""

# START_CLASS

	context = ContextReference()

	def __init__(self, context, arg=None, template=None):
		# arg is reference object
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.data = b""

	def read(self, stream):
		print("get pad")
		self.data = stream.read(self.get_pad(stream))

	def write(self, stream):
		self.data = ZERO * self.get_pad(stream)
		stream.write(self.data)

	def get_pad(self, stream):
		print("get pad")
		distance = stream.tell() - self.arg.io_start
		print("distance", distance)
		return get_padding_size(distance, alignment=self.template)

	def __repr__(self):
		return f"{self.data} Size: {len(self.data)}"
