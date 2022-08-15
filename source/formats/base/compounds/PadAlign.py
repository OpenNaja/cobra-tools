# START_GLOBALS
from generated.base_struct import BaseStruct
from modules.formats.shared import get_padding_size

ZERO = b"\x00"


# END_GLOBALS


class PadAlign(BaseStruct):
	"""Automatically aligns to template's start and pads so aligned with align"""

# START_CLASS

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data = b""

	def get_pad(self, stream):
		distance = stream.tell() - self.template.io_start
		return get_padding_size(distance, alignment=self.arg)

	def __repr__(self):
		return f"{self.data} Size: {len(self.data)}"

	@classmethod
	def read_fields(cls, stream, instance):
		instance.data = stream.read(instance.get_pad(stream))

	@classmethod
	def write_fields(cls, stream, instance):
		instance.data = ZERO * instance.get_pad(stream)
		stream.write(instance.data)
