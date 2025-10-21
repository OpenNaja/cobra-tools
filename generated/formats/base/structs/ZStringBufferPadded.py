from io import BytesIO
import logging

from generated.formats.base.basic import ZString
from generated.formats.base.structs.PadAlign import get_padding, get_padding_size

ZERO = b"\x00"


from generated.formats.base.structs.ZStringBuffer import ZStringBuffer


class ZStringBufferPadded(ZStringBuffer):

	"""
	Holds a buffer of zero-terminated strings, aligned to 8 bytes at the end
	"""

	__name__ = 'ZStringBufferPadded'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	def update_strings(self, list_of_strs):
		"""Updates this name buffer with a list of names"""
		super().update_strings(list_of_strs)
		self.data += get_padding(len(self.data), alignment=8)

