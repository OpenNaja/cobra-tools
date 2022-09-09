import numpy
from generated.array import Array
from generated.formats.base.basic import Uint64
from generated.formats.ms2.compounds.CommonJointInfo import CommonJointInfo
from generated.formats.ms2.compounds.HitCheckEntry import HitCheckEntry


class JointInfo(CommonJointInfo):

	__name__ = 'JointInfo'

	_import_path = 'generated.formats.ms2.compounds.JointInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 8 bytes of zeros
		self.zero = 0

		# 8 bytes of zeros per hitcheck
		self.zeros_per_hitcheck = Array(self.context, 0, None, (0,), Uint64)
		self.hitchecks = Array(self.context, 0, None, (0,), HitCheckEntry)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'zero', Uint64, (0, None), (False, None)
		yield 'zeros_per_hitcheck', Array, (0, None, (instance.hitcheck_count,), Uint64), (False, None)
		yield 'hitchecks', Array, (0, None, (instance.hitcheck_count,), HitCheckEntry), (False, None)
