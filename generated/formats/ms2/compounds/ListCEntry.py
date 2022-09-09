import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ms2.compounds.Vector3 import Vector3


class ListCEntry(BaseStruct):

	__name__ = 'ListCEntry'

	_import_key = 'ms2.compounds.ListCEntry'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 1 for carch and nasuto
		self.one = 0

		# center of the collider
		self.loc = Vector3(self.context, 0, None)

		# -1 for PZ, 80 for JWE
		self.constant = 0.0

		# ?
		self.a = 0.0

		# ?
		self.floats = Array(self.context, 0, None, (0,), Float)

		# sometimes repeat of a
		self.a_2 = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'one', Uint, (0, None), (False, None)
		yield 'loc', Vector3, (0, None), (False, None)
		yield 'constant', Float, (0, None), (False, None)
		yield 'a', Float, (0, None), (False, None)
		yield 'floats', Array, (0, None, (4,), Float), (False, None)
		yield 'a_2', Float, (0, None), (False, None)
