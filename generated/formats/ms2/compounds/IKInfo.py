from generated.base_struct import BaseStruct
from generated.formats.ms2.compounds.BonePointer import BonePointer
import logging

from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint64
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.ms2.compounds.IKEntry import IKEntry
from generated.formats.ms2.compounds.IKTarget import IKTarget
from generated.formats.ms2.compounds.UACJoint import UACJoint
from generated.formats.ovl_base.compounds.Empty import Empty
from generated.formats.ovl_base.compounds.SmartPadding import SmartPadding


class IKInfo(BaseStruct):

	__name__ = 'IKInfo'

	_import_key = 'ms2.compounds.IKInfo'

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

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('weird_padding', SmartPadding, (0, None), (False, None), (lambda context: context.version <= 13, None))
		yield ('ik_count', Uint64, (0, None), (False, None), (None, None))
		yield ('ik_ptr', Uint64, (0, None), (False, None), (None, None))
		yield ('ik_targets_count', Uint64, (0, None), (False, None), (lambda context: context.version >= 48, None))
		yield ('ik_targets_ptr', Uint64, (0, None), (False, None), (lambda context: context.version >= 48, None))
		yield ('ik_ref', Empty, (0, None), (False, None), (None, None))
		yield ('ik_list', Array, (0, None, (None,), UACJoint), (False, None), (lambda context: context.version <= 13, None))
		yield ('ik_list', Array, (0, None, (None,), IKEntry), (False, None), (lambda context: context.version >= 32, None))
		yield ('padding_0', PadAlign, (8, None), (False, None), (None, None))
		yield ('ik_targets', Array, (0, None, (None,), IKTarget), (False, None), (lambda context: context.version >= 50, None))
		yield ('padding_1', PadAlign, (8, None), (False, None), (lambda context: context.version >= 50, None))

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

	def get_pointers(self):
		"""Get all strings in the structure."""
		condition_function = lambda x: issubclass(x[1], BonePointer)
		for val in self.get_condition_values_recursive(self, condition_function):
			yield val

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		# after reading, we can resolve the bone pointers
		for ptr in instance.get_pointers():
			ptr.joint = instance.arg.bones[ptr.index]

	@classmethod
	def write_fields(cls, stream, instance):
		# update indices of bone pointers
		bones_map = {b: i for i, b in enumerate(instance.arg.bones)}
		for ptr in instance.get_pointers():
			ptr.index = bones_map.get(ptr.joint)
		super().write_fields(stream, instance)



IKInfo.init_attributes()
