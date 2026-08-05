# START_GLOBALS
import logging

from generated.formats.base.structs.PadAlign import PadAlign

# END_GLOBALS


class PadAlignFF(PadAlign):
	"""Automatically aligns to template's start and pads so aligned with align"""

# START_CLASS

	_PAD = b"\xFF"

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
