import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ms2.basic import OffsetString
from generated.formats.ms2.compounds.HitCheck import HitCheck


class JointInfo(BaseStruct):

	"""
	#ARG# is the names buffer
	the following defaults are all the same in PZ and JWE2 as of 2022-10-14
	"""

	__name__ = 'JointInfo'

	_import_key = 'ms2.compounds.JointInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.eleven = 11
		self.zero_0 = 0
		self.zero_1 = 0
		self.minus_1 = -1
		self.name = 0
		self.hitcheck_count = 0

		# 8 bytes of zeros
		self.zero_2 = 0

		# 8 bytes of zeros per hitcheck
		self.zeros_per_hitcheck = Array(self.context, 0, None, (0,), Uint64)
		self.hitchecks = Array(self.context, self.arg, None, (0,), HitCheck)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('eleven', Uint, (0, None), (False, 11), None),
		('zero_0', Int, (0, None), (False, 0), None),
		('zero_1', Int, (0, None), (False, 0), None),
		('minus_1', Int, (0, None), (False, -1), None),
		('name', OffsetString, (None, None), (False, None), None),
		('hitcheck_count', Uint, (0, None), (False, None), None),
		('zero_2', Uint64, (0, None), (False, None), None),
		('zeros_per_hitcheck', Array, (0, None, (None,), Uint64), (False, None), None),
		('hitchecks', Array, (None, None, (None,), HitCheck), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'eleven', Uint, (0, None), (False, 11)
		yield 'zero_0', Int, (0, None), (False, 0)
		yield 'zero_1', Int, (0, None), (False, 0)
		yield 'minus_1', Int, (0, None), (False, -1)
		yield 'name', OffsetString, (instance.arg, None), (False, None)
		yield 'hitcheck_count', Uint, (0, None), (False, None)
		yield 'zero_2', Uint64, (0, None), (False, None)
		yield 'zeros_per_hitcheck', Array, (0, None, (instance.hitcheck_count,), Uint64), (False, None)
		yield 'hitchecks', Array, (instance.arg, None, (instance.hitcheck_count,), HitCheck), (False, None)
