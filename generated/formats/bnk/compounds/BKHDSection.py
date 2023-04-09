import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint


class BKHDSection(BaseStruct):

	"""
	First Section of a soundbank aux
	"""

	__name__ = 'BKHDSection'

	_import_key = 'bnk.compounds.BKHDSection'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# length of following data
		self.length = 0
		self.version = 0
		self.id_a = 0
		self.id_b = 0
		self.constant_a = 0
		self.constant_b = 0
		self.unk = 0

		# sometimes present
		self.zeroes = Array(self.context, 0, None, (0,), Ubyte)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('length', Uint, (0, None), (False, None), (None, None))
		yield ('version', Uint, (0, None), (False, None), (None, None))
		yield ('id_a', Uint, (0, None), (False, None), (None, None))
		yield ('id_b', Uint, (0, None), (False, None), (None, None))
		yield ('constant_a', Uint, (0, None), (False, None), (None, None))
		yield ('constant_b', Uint, (0, None), (False, None), (None, None))
		yield ('unk', Uint, (0, None), (False, None), (None, None))
		yield ('zeroes', Array, (0, None, (None,), Ubyte), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'length', Uint, (0, None), (False, None)
		yield 'version', Uint, (0, None), (False, None)
		yield 'id_a', Uint, (0, None), (False, None)
		yield 'id_b', Uint, (0, None), (False, None)
		yield 'constant_a', Uint, (0, None), (False, None)
		yield 'constant_b', Uint, (0, None), (False, None)
		yield 'unk', Uint, (0, None), (False, None)
		yield 'zeroes', Array, (0, None, (instance.length - 24,), Ubyte), (False, None)
