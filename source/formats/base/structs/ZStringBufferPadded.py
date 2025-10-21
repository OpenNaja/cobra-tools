# START_GLOBALS
from io import BytesIO
import logging

from generated.formats.base.basic import ZString
from generated.formats.base.structs.PadAlign import get_padding, get_padding_size

ZERO = b"\x00"


# END_GLOBALS

class ZStringBufferPadded:
	"""Holds a buffer of zero-terminated strings, which can be accessed by their offset"""

# START_CLASS

	def update_strings(self, list_of_strs):
		"""Updates this name buffer with a list of names"""
		super().update_strings(list_of_strs)
		self.data += get_padding(len(self.data), alignment=8)
