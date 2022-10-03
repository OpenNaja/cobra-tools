import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Uint


class DATASection(BaseStruct):

	"""
	second Section of a soundback aux
	"""

	__name__ = 'DATASection'

	_import_key = 'bnk.compounds.DATASection'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# length of following data
		self.length = 0
		self.wem_datas = Array(self.context, 0, None, (0,), Byte)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('length', Uint, (0, None), (False, None), None),
		('wem_datas', Array, (0, None, (None,), Byte), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'length', Uint, (0, None), (False, None)
		yield 'wem_datas', Array, (0, None, (instance.length,), Byte), (False, None)
