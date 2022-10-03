import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint64
from generated.formats.ms2.compounds.NasutoJointEntry import NasutoJointEntry
from generated.formats.ms2.compounds.UACJoint import UACJoint
from generated.formats.ovl_base.compounds.SmartPadding import SmartPadding


class Struct7(BaseStruct):

	__name__ = 'Struct7'

	_import_key = 'ms2.compounds.Struct7'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# needed for ZTUAC
		self.weird_padding = SmartPadding(self.context, 0, None)

		# repeat
		self.count_7 = 0

		# seen 0
		self.zero_0 = 0

		# seen 0, 2, 4
		self.flag = 0
		self.zero_2 = 0

		# 36 bytes per entry

		# 60 bytes per entry
		self.unknown_list = Array(self.context, 0, None, (0,), NasutoJointEntry)

		# align list to multiples of 8
		self.padding = Array(self.context, 0, None, (0,), Ubyte)

		# latest PZ and jwe2 only - if flag is non-zero, 8 bytes, else 0
		self.alignment = 0
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('weird_padding', SmartPadding, (0, None), (False, None), True),
		('count_7', Uint64, (0, None), (False, None), None),
		('zero_0', Uint64, (0, None), (False, None), None),
		('flag', Uint64, (0, None), (False, None), True),
		('zero_2', Uint64, (0, None), (False, None), True),
		('unknown_list', Array, (0, None, (None,), UACJoint), (False, None), True),
		('unknown_list', Array, (0, None, (None,), NasutoJointEntry), (False, None), True),
		('padding', Array, (0, None, (None,), Ubyte), (False, None), None),
		('alignment', Uint64, (0, None), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version <= 13:
			yield 'weird_padding', SmartPadding, (0, None), (False, None)
		yield 'count_7', Uint64, (0, None), (False, None)
		yield 'zero_0', Uint64, (0, None), (False, None)
		if instance.context.version >= 48:
			yield 'flag', Uint64, (0, None), (False, None)
			yield 'zero_2', Uint64, (0, None), (False, None)
		if instance.context.version <= 13:
			yield 'unknown_list', Array, (0, None, (instance.count_7,), UACJoint), (False, None)
		if instance.context.version >= 32:
			yield 'unknown_list', Array, (0, None, (instance.count_7,), NasutoJointEntry), (False, None)
		yield 'padding', Array, (0, None, ((8 - ((instance.count_7 * 60) % 8)) % 8,), Ubyte), (False, None)
		if instance.context.version >= 50 and instance.flag:
			yield 'alignment', Uint64, (0, None), (False, None)
