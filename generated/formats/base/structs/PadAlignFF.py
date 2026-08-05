import logging

from generated.formats.base.structs.PadAlign import PadAlign

from generated.base_struct import BaseStruct


class PadAlignFF(PadAlign, BaseStruct):

	"""
	Grabs as many bytes as needed to align #ARG# bytes from the start of #TEMPLATE#
	"""

	__name__ = 'PadAlignFF'


	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)

	_PAD = b"\xFF"

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

