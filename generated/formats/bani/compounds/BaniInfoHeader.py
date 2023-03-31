import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.bani.compounds.BaniRoot import BaniRoot
from generated.formats.base.basic import Byte
from generated.formats.base.basic import ZString


class BaniInfoHeader(BaseStruct):

	"""
	Custom header struct
	includes fragments but none of the 3 data buffers
	"""

	__name__ = 'BaniInfoHeader'

	_import_key = 'bani.compounds.BaniInfoHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 'BANI'
		self.magic = Array(self.context, 0, None, (0,), Byte)

		# name of the banis file buffer
		self.banis_name = ''
		self.data = BaniRoot(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('magic', Array, (0, None, (4,), Byte), (False, None), None)
		yield ('banis_name', ZString, (0, None), (False, None), None)
		yield ('data', BaniRoot, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'magic', Array, (0, None, (4,), Byte), (False, None)
		yield 'banis_name', ZString, (0, None), (False, None)
		yield 'data', BaniRoot, (0, None), (False, None)


BaniInfoHeader.init_attributes()
