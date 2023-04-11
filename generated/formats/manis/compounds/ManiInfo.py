from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.manis.imports import name_type_map


class ManiInfo(BaseStruct):

	"""
	288 bytes for JWE / PZ
	304 bytes for PC
	"""

	__name__ = 'ManiInfo'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.duration = name_type_map['Float'](self.context, 0, None)
		self.frame_count = name_type_map['Uint'](self.context, 0, None)

		# ?
		self.b = name_type_map['Uint'](self.context, 0, None)
		self.zeros_0 = Array(self.context, 0, None, (0,), name_type_map['Ushort'])
		self.extra_pc_1 = name_type_map['Ushort'](self.context, 0, None)
		self.pos_bone_count = name_type_map['Ushort'](self.context, 0, None)
		self.ori_bone_count = name_type_map['Ushort'](self.context, 0, None)

		# likely
		self.scl_bone_count = name_type_map['Ushort'](self.context, 0, None)

		# zero
		self.extra_pc = name_type_map['Uint64'](self.context, 0, None)
		self.pos_bone_count_repeat = name_type_map['Ushort'](self.context, 0, None)
		self.ori_bone_count_repeat = name_type_map['Ushort'](self.context, 0, None)
		self.scl_bone_count_repeat = name_type_map['Ushort'](self.context, 0, None)
		self.zeros_1 = name_type_map['Ushort'](self.context, 0, None)
		self.zeros_1_new = name_type_map['Uint'](self.context, 0, None)
		self.float_count = name_type_map['Ushort'](self.context, 0, None)

		# FF if unused
		self.count_a = name_type_map['Ubyte'](self.context, 0, None)

		# FF if unused
		self.count_b = name_type_map['Ubyte'](self.context, 0, None)

		# usually matches ms2 bone count, at least for JWE2 dinos. Doesn't match for PZ water wheel 5 vs ms2 2
		self.target_bone_count = name_type_map['Ushort'](self.context, 0, None)

		# zero
		self.g = name_type_map['Ushort'](self.context, 0, None)

		# rest 228 bytes
		self.zeros_2 = Array(self.context, 0, None, (0,), name_type_map['Uint'])

		# rest 14 bytes
		self.extra_zeros_pc = Array(self.context, 0, None, (0,), name_type_map['Ushort'])
		self.pos_bone_min = name_type_map['Ubyte'](self.context, 0, None)
		self.pos_bone_max = name_type_map['Ubyte'](self.context, 0, None)
		self.ori_bone_min = name_type_map['Ubyte'](self.context, 0, None)
		self.ori_bone_max = name_type_map['Ubyte'](self.context, 0, None)

		# always FF
		self.scl_bone_min = name_type_map['Byte'](self.context, 0, None)

		# always 00
		self.scl_bone_max = name_type_map['Byte'](self.context, 0, None)
		self.pos_bone_count_related = name_type_map['Ubyte'](self.context, 0, None)
		self.pos_bone_count_repeat = name_type_map['Ubyte'](self.context, 0, None)
		self.ori_bone_count_related = name_type_map['Ubyte'](self.context, 0, None)
		self.ori_bone_count_repeat = name_type_map['Ubyte'](self.context, 0, None)

		# maybe, not observed yet
		self.scl_bone_count_related = name_type_map['Byte'](self.context, 0, None)
		self.scl_bone_count_repeat = name_type_map['Byte'](self.context, 0, None)
		self.zeros_end = name_type_map['Ushort'](self.context, 0, None)
		self.zero_2_end = name_type_map['Ushort'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'duration', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'frame_count', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'b', name_type_map['Uint'], (0, None), (False, None), (None, None)
		yield 'zeros_0', Array, (0, None, (6,), name_type_map['Ushort']), (False, None), (None, None)
		yield 'extra_pc_1', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version <= 257, None)
		yield 'pos_bone_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'ori_bone_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'scl_bone_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'extra_pc', name_type_map['Uint64'], (0, None), (False, None), (lambda context: context.version <= 257, None)
		yield 'pos_bone_count_repeat', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version <= 257, None)
		yield 'ori_bone_count_repeat', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version <= 257, None)
		yield 'scl_bone_count_repeat', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version <= 257, None)
		yield 'zeros_1', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'zeros_1_new', name_type_map['Uint'], (0, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'float_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'count_a', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'count_b', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'target_bone_count', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'g', name_type_map['Ushort'], (0, None), (False, None), (None, None)
		yield 'zeros_2', Array, (0, None, (57,), name_type_map['Uint']), (False, None), (None, None)
		yield 'extra_zeros_pc', Array, (0, None, (6,), name_type_map['Ushort']), (False, None), (lambda context: context.version <= 257, None)
		yield 'pos_bone_min', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'pos_bone_max', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'ori_bone_min', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'ori_bone_max', name_type_map['Ubyte'], (0, None), (False, None), (None, None)
		yield 'scl_bone_min', name_type_map['Byte'], (0, None), (False, None), (None, None)
		yield 'scl_bone_max', name_type_map['Byte'], (0, None), (False, None), (None, None)
		yield 'pos_bone_count_related', name_type_map['Ubyte'], (0, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'pos_bone_count_repeat', name_type_map['Ubyte'], (0, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'ori_bone_count_related', name_type_map['Ubyte'], (0, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'ori_bone_count_repeat', name_type_map['Ubyte'], (0, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'scl_bone_count_related', name_type_map['Byte'], (0, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'scl_bone_count_repeat', name_type_map['Byte'], (0, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'zeros_end', name_type_map['Ushort'], (0, None), (False, None), (lambda context: context.version >= 258, None)
		yield 'zero_2_end', name_type_map['Ushort'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'duration', name_type_map['Float'], (0, None), (False, None)
		yield 'frame_count', name_type_map['Uint'], (0, None), (False, None)
		yield 'b', name_type_map['Uint'], (0, None), (False, None)
		yield 'zeros_0', Array, (0, None, (6,), name_type_map['Ushort']), (False, None)
		if instance.context.version <= 257:
			yield 'extra_pc_1', name_type_map['Ushort'], (0, None), (False, None)
		yield 'pos_bone_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'ori_bone_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'scl_bone_count', name_type_map['Ushort'], (0, None), (False, None)
		if instance.context.version <= 257:
			yield 'extra_pc', name_type_map['Uint64'], (0, None), (False, None)
			yield 'pos_bone_count_repeat', name_type_map['Ushort'], (0, None), (False, None)
			yield 'ori_bone_count_repeat', name_type_map['Ushort'], (0, None), (False, None)
			yield 'scl_bone_count_repeat', name_type_map['Ushort'], (0, None), (False, None)
		yield 'zeros_1', name_type_map['Ushort'], (0, None), (False, None)
		if instance.context.version >= 258:
			yield 'zeros_1_new', name_type_map['Uint'], (0, None), (False, None)
		yield 'float_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'count_a', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'count_b', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'target_bone_count', name_type_map['Ushort'], (0, None), (False, None)
		yield 'g', name_type_map['Ushort'], (0, None), (False, None)
		yield 'zeros_2', Array, (0, None, (57,), name_type_map['Uint']), (False, None)
		if instance.context.version <= 257:
			yield 'extra_zeros_pc', Array, (0, None, (6,), name_type_map['Ushort']), (False, None)
		yield 'pos_bone_min', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'pos_bone_max', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'ori_bone_min', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'ori_bone_max', name_type_map['Ubyte'], (0, None), (False, None)
		yield 'scl_bone_min', name_type_map['Byte'], (0, None), (False, None)
		yield 'scl_bone_max', name_type_map['Byte'], (0, None), (False, None)
		if instance.context.version >= 258:
			yield 'pos_bone_count_related', name_type_map['Ubyte'], (0, None), (False, None)
			yield 'pos_bone_count_repeat', name_type_map['Ubyte'], (0, None), (False, None)
			yield 'ori_bone_count_related', name_type_map['Ubyte'], (0, None), (False, None)
			yield 'ori_bone_count_repeat', name_type_map['Ubyte'], (0, None), (False, None)
			yield 'scl_bone_count_related', name_type_map['Byte'], (0, None), (False, None)
			yield 'scl_bone_count_repeat', name_type_map['Byte'], (0, None), (False, None)
			yield 'zeros_end', name_type_map['Ushort'], (0, None), (False, None)
		yield 'zero_2_end', name_type_map['Ushort'], (0, None), (False, None)
