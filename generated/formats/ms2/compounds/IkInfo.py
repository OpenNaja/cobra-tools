from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.ms2.compounds.IKEntry import IKEntry
from generated.formats.ms2.compounds.IKTarget import IKTarget
from generated.formats.ms2.compounds.UACJoint import UACJoint
from generated.formats.ovl_base.compounds.Empty import Empty
from generated.formats.ovl_base.compounds.SmartPadding import SmartPadding


class IkInfo(BaseStruct):

	__name__ = 'IK_Info'

	_import_key = 'ms2.compounds.IkInfo'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# needed for ZTUAC
		self.weird_padding = SmartPadding(self.context, 0, None)

		# repeat
		self.ik_count = 0
		self.ik_ptr = 0

		# seen 0, 2, 4
		self.ik_targets_count = 0
		self.ik_targets_ptr = 0
		self.ik_ref = Empty(self.context, 0, None)
		self.ik_list = Array(self.context, 0, None, (0,), IKEntry)
		self.padding_0 = PadAlign(self.context, 8, self.ik_ref)
		self.ik_targets = Array(self.context, 0, None, (0,), IKTarget)
		self.padding_1 = PadAlign(self.context, 8, self.ik_ref)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('weird_padding', SmartPadding, (0, None), (False, None), True),
		('ik_count', Uint64, (0, None), (False, None), None),
		('ik_ptr', Uint64, (0, None), (False, None), None),
		('ik_targets_count', Uint64, (0, None), (False, None), True),
		('ik_targets_ptr', Uint64, (0, None), (False, None), True),
		('ik_ref', Empty, (0, None), (False, None), None),
		('ik_list', Array, (0, None, (None,), UACJoint), (False, None), True),
		('ik_list', Array, (0, None, (None,), IKEntry), (False, None), True),
		('padding_0', PadAlign, (8, None), (False, None), None),
		('ik_targets', Array, (0, None, (None,), IKTarget), (False, None), True),
		('padding_1', PadAlign, (8, None), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version <= 13:
			yield 'weird_padding', SmartPadding, (0, None), (False, None)
		yield 'ik_count', Uint64, (0, None), (False, None)
		yield 'ik_ptr', Uint64, (0, None), (False, None)
		if instance.context.version >= 48:
			yield 'ik_targets_count', Uint64, (0, None), (False, None)
			yield 'ik_targets_ptr', Uint64, (0, None), (False, None)
		yield 'ik_ref', Empty, (0, None), (False, None)
		if instance.context.version <= 13:
			yield 'ik_list', Array, (0, None, (instance.ik_count,), UACJoint), (False, None)
		if instance.context.version >= 32:
			yield 'ik_list', Array, (0, None, (instance.ik_count,), IKEntry), (False, None)
		yield 'padding_0', PadAlign, (8, instance.ik_ref), (False, None)
		if instance.context.version >= 50:
			yield 'ik_targets', Array, (0, None, (instance.ik_targets_count,), IKTarget), (False, None)
			yield 'padding_1', PadAlign, (8, instance.ik_ref), (False, None)
