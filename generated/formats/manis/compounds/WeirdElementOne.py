import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64


class WeirdElementOne(BaseStruct):

	__name__ = 'WeirdElementOne'

	_import_key = 'manis.compounds.WeirdElementOne'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.float_0 = 0.0
		self.zero_0 = 0
		self.floats_0 = Array(self.context, 0, None, (0,), Float)
		self.zeros_0 = Array(self.context, 0, None, (0,), Uint64)
		self.floats_1 = Array(self.context, 0, None, (0,), Float)
		self.countb = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('float_0', Float, (0, None), (False, None), None)
		yield ('zero_0', Uint, (0, None), (False, None), None)
		yield ('floats_0', Array, (0, None, (2,), Float), (False, None), None)
		yield ('zeros_0', Array, (0, None, (2,), Uint64), (False, None), None)
		yield ('floats_1', Array, (0, None, (3,), Float), (False, None), None)
		yield ('countb', Uint, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'float_0', Float, (0, None), (False, None)
		yield 'zero_0', Uint, (0, None), (False, None)
		yield 'floats_0', Array, (0, None, (2,), Float), (False, None)
		yield 'zeros_0', Array, (0, None, (2,), Uint64), (False, None)
		yield 'floats_1', Array, (0, None, (3,), Float), (False, None)
		yield 'countb', Uint, (0, None), (False, None)


WeirdElementOne.init_attributes()
