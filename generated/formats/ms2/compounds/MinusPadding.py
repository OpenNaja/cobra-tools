import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Short


class MinusPadding(BaseStruct):

	"""
	Used in PC
	"""

	__name__ = 'MinusPadding'

	_import_key = 'ms2.compounds.MinusPadding'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# -1
		self.indices = Array(self.context, 0, None, (0,), Short)

		# 0
		self.padding = Array(self.context, 0, None, (0,), Byte)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'indices', Array, (0, None, (instance.arg,), Short), (False, None)
		yield 'padding', Array, (0, None, ((16 - ((instance.arg * 2) % 16)) % 16,), Byte), (False, None)
