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
	"""

	__name__ = 'JointInfo'

	_import_key = 'ms2.compounds.JointInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# must be 11
		self.eleven = 0

		# bunch of -1's
		self.f_fs = Array(self.context, 0, None, (0,), Int)
		self.name = 0
		self.hitcheck_count = 0

		# 8 bytes of zeros
		self.zero = 0

		# 8 bytes of zeros per hitcheck
		self.zeros_per_hitcheck = Array(self.context, 0, None, (0,), Uint64)
		self.hitchecks = Array(self.context, self.arg, None, (0,), HitCheck)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'eleven', Uint, (0, None), (False, None)
		yield 'f_fs', Array, (0, None, (3,), Int), (False, None)
		yield 'name', OffsetString, (instance.arg, None), (False, None)
		yield 'hitcheck_count', Uint, (0, None), (False, None)
		yield 'zero', Uint64, (0, None), (False, None)
		yield 'zeros_per_hitcheck', Array, (0, None, (instance.hitcheck_count,), Uint64), (False, None)
		yield 'hitchecks', Array, (instance.arg, None, (instance.hitcheck_count,), HitCheck), (False, None)
