import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Byte
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort


class ManiInfo(BaseStruct):

	"""
	288 bytes for JWE / PZ
	304 bytes for PC
	"""

	__name__ = 'ManiInfo'

	_import_key = 'manis.compounds.ManiInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.duration = 0.0
		self.frame_count = 0

		# ?
		self.b = 0
		self.zeros_0 = Array(self.context, 0, None, (0,), Ushort)
		self.extra_pc_1 = 0
		self.pos_bone_count = 0
		self.ori_bone_count = 0

		# likely
		self.scl_bone_count = 0

		# zero
		self.extra_pc = 0
		self.pos_bone_count_repeat = 0
		self.ori_bone_count_repeat = 0
		self.scl_bone_count_repeat = 0
		self.zeros_1 = 0
		self.zeros_1_new = 0
		self.float_count = 0

		# FF if unused
		self.count_a = 0

		# FF if unused
		self.count_b = 0

		# usually matches ms2 bone count, at least for JWE2 dinos. Doesn't match for PZ water wheel 5 vs ms2 2
		self.target_bone_count = 0

		# zero
		self.g = 0

		# rest 228 bytes
		self.zeros_2 = Array(self.context, 0, None, (0,), Uint)

		# rest 14 bytes
		self.extra_zeros_pc = Array(self.context, 0, None, (0,), Ushort)
		self.pos_bone_min = 0
		self.pos_bone_max = 0
		self.ori_bone_min = 0
		self.ori_bone_max = 0

		# always FF
		self.scl_bone_min = 0

		# always 00
		self.scl_bone_max = 0
		self.pos_bone_count_related = 0
		self.pos_bone_count_repeat = 0
		self.ori_bone_count_related = 0
		self.ori_bone_count_repeat = 0

		# maybe, not observed yet
		self.scl_bone_count_related = 0
		self.scl_bone_count_repeat = 0
		self.zeros_end = 0
		self.zero_2_end = 0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'duration', Float, (0, None), (False, None)
		yield 'frame_count', Uint, (0, None), (False, None)
		yield 'b', Uint, (0, None), (False, None)
		yield 'zeros_0', Array, (0, None, (6,), Ushort), (False, None)
		if instance.context.version <= 257:
			yield 'extra_pc_1', Ushort, (0, None), (False, None)
		yield 'pos_bone_count', Ushort, (0, None), (False, None)
		yield 'ori_bone_count', Ushort, (0, None), (False, None)
		yield 'scl_bone_count', Ushort, (0, None), (False, None)
		if instance.context.version <= 257:
			yield 'extra_pc', Uint64, (0, None), (False, None)
			yield 'pos_bone_count_repeat', Ushort, (0, None), (False, None)
			yield 'ori_bone_count_repeat', Ushort, (0, None), (False, None)
			yield 'scl_bone_count_repeat', Ushort, (0, None), (False, None)
		yield 'zeros_1', Ushort, (0, None), (False, None)
		if instance.context.version >= 258:
			yield 'zeros_1_new', Uint, (0, None), (False, None)
		yield 'float_count', Ushort, (0, None), (False, None)
		yield 'count_a', Ubyte, (0, None), (False, None)
		yield 'count_b', Ubyte, (0, None), (False, None)
		yield 'target_bone_count', Ushort, (0, None), (False, None)
		yield 'g', Ushort, (0, None), (False, None)
		yield 'zeros_2', Array, (0, None, (57,), Uint), (False, None)
		if instance.context.version <= 257:
			yield 'extra_zeros_pc', Array, (0, None, (6,), Ushort), (False, None)
		yield 'pos_bone_min', Ubyte, (0, None), (False, None)
		yield 'pos_bone_max', Ubyte, (0, None), (False, None)
		yield 'ori_bone_min', Ubyte, (0, None), (False, None)
		yield 'ori_bone_max', Ubyte, (0, None), (False, None)
		yield 'scl_bone_min', Byte, (0, None), (False, None)
		yield 'scl_bone_max', Byte, (0, None), (False, None)
		if instance.context.version >= 258:
			yield 'pos_bone_count_related', Ubyte, (0, None), (False, None)
			yield 'pos_bone_count_repeat', Ubyte, (0, None), (False, None)
			yield 'ori_bone_count_related', Ubyte, (0, None), (False, None)
			yield 'ori_bone_count_repeat', Ubyte, (0, None), (False, None)
			yield 'scl_bone_count_related', Byte, (0, None), (False, None)
			yield 'scl_bone_count_repeat', Byte, (0, None), (False, None)
			yield 'zeros_end', Ushort, (0, None), (False, None)
		yield 'zero_2_end', Ushort, (0, None), (False, None)
