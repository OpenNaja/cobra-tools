import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.manis.compounds.FloatsGrabber import FloatsGrabber
from generated.formats.manis.compounds.Repeat import Repeat
from generated.formats.ovl_base.compounds.Empty import Empty
from generated.formats.ovl_base.compounds.SmartPadding import SmartPadding


class CompressedManiData(BaseStruct):

	__name__ = 'CompressedManiData'

	_import_key = 'manis.compounds.CompressedManiData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.ref = Empty(self.context, 0, None)

		# these are likely a scale reference or factor
		self.floatsa = Array(self.context, 0, None, (0,), Float)

		# ?
		self.pad_2 = SmartPadding(self.context, 0, None)
		self.frame_count = 0
		self.ori_bone_count = 0
		self.pos_bone_count = 0

		# maybe
		self.scl_bone_count = 0

		# fixed
		self.zeros_18 = Array(self.context, 0, None, (0,), Uint)
		self.count = 0

		# usually 420, or 0
		self.quantisation_level = 0
		self.ref_2 = Empty(self.context, 0, None)
		self.some_indices = Array(self.context, 0, None, (0,), Ubyte)
		self.flag_0 = 0
		self.flag_1 = 0
		self.flag_2 = 0
		self.flag_3 = 0
		self.anoth_pad = PadAlign(self.context, 4, self.ref_2)

		# these are likely a scale reference or factor
		self.floatsb = FloatsGrabber(self.context, 0, None)

		# this seems to be vaguely related, but not always there?
		self.extra_pc_zero = 0
		self.anoth_pad_2 = PadAlign(self.context, 16, self.ref)
		self.ref_3 = Empty(self.context, 0, None)
		self.repeats = Array(self.context, 0, None, (0,), Repeat)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('ref', Empty, (0, None), (False, None), None),
		('floatsa', Array, (0, None, (None, None,), Float), (False, None), None),
		('pad_2', SmartPadding, (0, None), (False, None), None),
		('frame_count', Uint, (0, None), (False, None), None),
		('ori_bone_count', Uint, (0, None), (False, None), None),
		('pos_bone_count', Uint, (0, None), (False, None), None),
		('scl_bone_count', Uint, (0, None), (False, None), None),
		('zeros_18', Array, (0, None, (18,), Uint), (False, None), None),
		('count', Ushort, (0, None), (False, None), None),
		('quantisation_level', Ushort, (0, None), (False, None), None),
		('ref_2', Empty, (0, None), (False, None), None),
		('some_indices', Array, (0, None, (None,), Ubyte), (False, None), None),
		('flag_0', Ubyte, (0, None), (False, None), None),
		('flag_1', Ubyte, (0, None), (False, None), None),
		('flag_2', Ubyte, (0, None), (False, None), None),
		('flag_3', Ubyte, (0, None), (False, None), None),
		('anoth_pad', PadAlign, (4, None), (False, None), None),
		('floatsb', FloatsGrabber, (0, None), (False, None), None),
		('extra_pc_zero', Uint64, (0, None), (False, None), True),
		('anoth_pad_2', PadAlign, (16, None), (False, None), None),
		('ref_3', Empty, (0, None), (False, None), None),
		('repeats', Array, (0, None, (None,), Repeat), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'ref', Empty, (0, None), (False, None)
		yield 'floatsa', Array, (0, None, (instance.arg.frame_count, instance.arg.float_count,), Float), (False, None)
		yield 'pad_2', SmartPadding, (0, None), (False, None)
		yield 'frame_count', Uint, (0, None), (False, None)
		yield 'ori_bone_count', Uint, (0, None), (False, None)
		yield 'pos_bone_count', Uint, (0, None), (False, None)
		yield 'scl_bone_count', Uint, (0, None), (False, None)
		yield 'zeros_18', Array, (0, None, (18,), Uint), (False, None)
		yield 'count', Ushort, (0, None), (False, None)
		yield 'quantisation_level', Ushort, (0, None), (False, None)
		yield 'ref_2', Empty, (0, None), (False, None)
		yield 'some_indices', Array, (0, None, (instance.pos_bone_count,), Ubyte), (False, None)
		yield 'flag_0', Ubyte, (0, None), (False, None)
		yield 'flag_1', Ubyte, (0, None), (False, None)
		yield 'flag_2', Ubyte, (0, None), (False, None)
		yield 'flag_3', Ubyte, (0, None), (False, None)
		yield 'anoth_pad', PadAlign, (4, instance.ref_2), (False, None)
		yield 'floatsb', FloatsGrabber, (0, None), (False, None)
		if instance.context.version <= 257:
			yield 'extra_pc_zero', Uint64, (0, None), (False, None)
		yield 'anoth_pad_2', PadAlign, (16, instance.ref), (False, None)
		yield 'ref_3', Empty, (0, None), (False, None)
		yield 'repeats', Array, (0, None, (instance.count,), Repeat), (False, None)
