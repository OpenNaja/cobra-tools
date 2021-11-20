# START_GLOBALS
from generated.io import MAX_LEN
from modules.formats.shared import get_padding_size

ZERO = b"\x00"


# END_GLOBALS

class PadAlign:
	"""Automatically aligns to template's start and pads so aligned with arg"""

# START_CLASS

	def __init__(self, context, arg=0, template=None):
		self._context = context
		self.arg = arg
		# template is reference object
		self.template = template
		self.data = b""

	def read(self, stream):
		self.data = stream.read(self.get_pad(stream))

	def write(self, stream):
		self.data = ZERO * self.get_pad(stream)
		stream.write(self.data)

	def get_pad(self, stream):
		distance = stream.tell() - self.template.io_start
		return get_padding_size(distance, alignment=self.arg)

	def __repr__(self):
		return f"{self.data} Size: {len(self.data)}"
