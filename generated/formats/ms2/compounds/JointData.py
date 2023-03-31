from generated.base_struct import BaseStruct
from generated.formats.ms2.basic import OffsetString
from generated.formats.ms2.compounds.JointPointer import JointPointer
import logging

import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.compounds.PadAlign import PadAlign
from generated.formats.base.compounds.ZStringBuffer import ZStringBuffer
from generated.formats.ms2.compounds.HitcheckReader import HitcheckReader
from generated.formats.ms2.compounds.JointInfo import JointInfo
from generated.formats.ms2.compounds.JointTransform import JointTransform
from generated.formats.ms2.compounds.PushConstraint import PushConstraint
from generated.formats.ms2.compounds.RagdollConstraint import RagdollConstraint
from generated.formats.ms2.compounds.RigidBody import RigidBody
from generated.formats.ms2.compounds.StretchConstraint import StretchConstraint
from generated.formats.ms2.compounds.UACJointFF import UACJointFF
from generated.formats.ovl_base.compounds.Empty import Empty
from generated.formats.ovl_base.compounds.SmartPadding import SmartPadding


class JointData(BaseStruct):

	__name__ = 'JointData'

	_import_key = 'ms2.compounds.JointData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# seemingly additional alignment, unsure about the rule
		self.start_pc = SmartPadding(self.context, 0, None)
		self.before_dla_0 = 0
		self.before_dla_1 = 0

		# repeat
		self.joint_count = 0
		self.num_push_constraints = 0
		self.num_stretch_constraints = 0
		self.num_ragdoll_constraints = 0
		self.zero_0 = 0
		self.zero_1 = 0

		# size of the name buffer below, including trailing zeros
		self.namespace_length = 0

		# 0s
		self.zeros_0 = Array(self.context, 0, None, (0,), Uint)

		# 0 or 1
		self.pc_count = 0

		# 0s
		self.zeros_1 = Array(self.context, 0, None, (0,), Uint)

		# 0s
		self.extra_zeros_2 = Array(self.context, 0, None, (0,), Uint)
		self.one_0 = 1
		self.one_1 = 1

		# matches bone count from bone info
		self.bone_count = 0
		self.joint_entry_count = 0

		# usually 0s
		self.zeros_2 = Array(self.context, 0, None, (0,), Uint)

		# usually 0s
		self.zeros_3 = 0
		self.names_ref = Empty(self.context, 0, None)

		# corresponds to bone transforms
		self.joint_transforms = Array(self.context, 0, None, (0,), JointTransform)
		self.rigid_body_pointers = Array(self.context, 0, None, (0,), Uint64)
		self.rigid_body_list = Array(self.context, 0, None, (0,), RigidBody)
		self.push_constraints = Array(self.context, 0, None, (0,), PushConstraint)
		self.stretch_constraints = Array(self.context, 0, None, (0,), StretchConstraint)
		self.ragdoll_constraints = Array(self.context, 0, None, (0,), RagdollConstraint)

		# old style - joint infos, without hitchecks, they are added later
		self.joint_infos = Array(self.context, 0, None, (0,), UACJointFF)

		# sometimes an array of floats
		self.pc_floats = Array(self.context, 0, None, (0,), Float)

		# index into bone info bones for each joint; bone that the joint is attached to
		self.joint_to_bone = Array(self.context, 0, None, (0,), Int)

		# the inverse of the above; for each bone info bone, index of the corresponding joint or -1 if no joint
		self.bone_to_joint = Array(self.context, 0, None, (0,), Int)
		self.joint_names = ZStringBuffer(self.context, self.namespace_length, None)

		# the padding goes wrong on 144 because its first hitcheck has collision type 0
		self.joint_names_padding = SmartPadding(self.context, 0, None)

		# new style - includes name offset, some flags and the hitchecks
		self.joint_infos = Array(self.context, self.joint_names, None, (0,), JointInfo)

		# old style - for each joint, read the hitchecks
		self.hitcheck_reader = HitcheckReader(self.context, self, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('start_pc', SmartPadding, (0, None), (False, None), (lambda context: context.version == 32, None))
		yield ('before_dla_0', Uint64, (0, None), (False, None), (lambda context: context.version <= 7, None))
		yield ('before_dla_1', Uint64, (0, None), (False, None), (lambda context: context.version <= 7, None))
		yield ('joint_count', Uint, (0, None), (False, None), (None, None))
		yield ('num_push_constraints', Uint, (0, None), (False, None), (None, None))
		yield ('num_stretch_constraints', Uint, (0, None), (False, None), (None, None))
		yield ('num_ragdoll_constraints', Uint, (0, None), (False, None), (None, None))
		yield ('zero_0', Uint, (0, None), (False, None), (lambda context: context.version <= 32, None))
		yield ('zero_1', Uint, (0, None), (False, None), (lambda context: 13 <= context.version <= 32, None))
		yield ('namespace_length', Uint, (0, None), (False, None), (None, None))
		yield ('zeros_0', Array, (0, None, (5,), Uint), (False, None), (None, None))
		yield ('pc_count', Uint, (0, None), (False, None), (None, None))
		yield ('zeros_1', Array, (0, None, (7,), Uint), (False, None), (None, None))
		yield ('extra_zeros_2', Array, (0, None, (4,), Uint), (False, None), (lambda context: 13 <= context.version <= 32, None))
		yield ('one_0', Uint64, (0, None), (False, 1), (lambda context: context.version >= 13, None))
		yield ('one_1', Uint64, (0, None), (False, 1), (lambda context: context.version >= 13, None))
		yield ('bone_count', Uint, (0, None), (False, None), (None, None))
		yield ('joint_entry_count', Uint, (0, None), (False, None), (None, None))
		yield ('zeros_2', Array, (0, None, (4,), Uint), (False, None), (None, None))
		yield ('zeros_3', Uint, (0, None), (False, None), (lambda context: context.version <= 7, None))
		yield ('names_ref', Empty, (0, None), (False, None), (None, None))
		yield ('joint_transforms', Array, (0, None, (None,), JointTransform), (False, None), (None, None))
		yield ('rigid_body_pointers', Array, (0, None, (None,), Uint64), (False, None), (lambda context: context.version >= 47, None))
		yield ('rigid_body_list', Array, (0, None, (None,), RigidBody), (False, None), (lambda context: context.version >= 47, None))
		yield ('push_constraints', Array, (0, None, (None,), PushConstraint), (False, None), (lambda context: context.version >= 47, None))
		yield ('stretch_constraints', Array, (0, None, (None,), StretchConstraint), (False, None), (lambda context: context.version >= 47, None))
		yield ('ragdoll_constraints', Array, (0, None, (None,), RagdollConstraint), (False, None), (lambda context: context.version >= 47, None))
		yield ('joint_infos', Array, (0, None, (None,), UACJointFF), (False, None), (lambda context: context.version <= 32, None))
		yield ('pc_floats', Array, (0, None, (None, 10,), Float), (False, None), (lambda context: context.version <= 32, None))
		yield ('joint_to_bone', Array, (0, None, (None,), Int), (False, None), (None, None))
		yield ('bone_to_joint', Array, (0, None, (None,), Int), (False, None), (None, None))
		yield ('joint_names', ZStringBuffer, (None, None), (False, None), (None, None))
		yield ('joint_names_padding', PadAlign, (8, None), (False, None), (lambda context: context.version >= 47, None))
		yield ('joint_names_padding', SmartPadding, (0, None), (False, None), (lambda context: context.version <= 32, None))
		yield ('joint_infos', Array, (None, None, (None,), JointInfo), (False, None), (lambda context: context.version >= 47, None))
		yield ('hitcheck_reader', HitcheckReader, (None, None), (False, None), (lambda context: context.version <= 32, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version == 32:
			yield 'start_pc', SmartPadding, (0, None), (False, None)
		if instance.context.version <= 7:
			yield 'before_dla_0', Uint64, (0, None), (False, None)
			yield 'before_dla_1', Uint64, (0, None), (False, None)
		yield 'joint_count', Uint, (0, None), (False, None)
		yield 'num_push_constraints', Uint, (0, None), (False, None)
		yield 'num_stretch_constraints', Uint, (0, None), (False, None)
		yield 'num_ragdoll_constraints', Uint, (0, None), (False, None)
		if instance.context.version <= 32:
			yield 'zero_0', Uint, (0, None), (False, None)
		if 13 <= instance.context.version <= 32:
			yield 'zero_1', Uint, (0, None), (False, None)
		yield 'namespace_length', Uint, (0, None), (False, None)
		yield 'zeros_0', Array, (0, None, (5,), Uint), (False, None)
		yield 'pc_count', Uint, (0, None), (False, None)
		yield 'zeros_1', Array, (0, None, (7,), Uint), (False, None)
		if 13 <= instance.context.version <= 32:
			yield 'extra_zeros_2', Array, (0, None, (4,), Uint), (False, None)
		if instance.context.version >= 13:
			yield 'one_0', Uint64, (0, None), (False, 1)
			yield 'one_1', Uint64, (0, None), (False, 1)
		yield 'bone_count', Uint, (0, None), (False, None)
		yield 'joint_entry_count', Uint, (0, None), (False, None)
		yield 'zeros_2', Array, (0, None, (4,), Uint), (False, None)
		if instance.context.version <= 7:
			yield 'zeros_3', Uint, (0, None), (False, None)
		yield 'names_ref', Empty, (0, None), (False, None)
		yield 'joint_transforms', Array, (0, None, (instance.joint_count,), JointTransform), (False, None)
		if instance.context.version >= 47:
			yield 'rigid_body_pointers', Array, (0, None, (instance.joint_count,), Uint64), (False, None)
			yield 'rigid_body_list', Array, (0, None, (instance.joint_count,), RigidBody), (False, None)
			yield 'push_constraints', Array, (0, None, (instance.num_push_constraints,), PushConstraint), (False, None)
			yield 'stretch_constraints', Array, (0, None, (instance.num_stretch_constraints,), StretchConstraint), (False, None)
			yield 'ragdoll_constraints', Array, (0, None, (instance.num_ragdoll_constraints,), RagdollConstraint), (False, None)
		if instance.context.version <= 32:
			yield 'joint_infos', Array, (0, None, (instance.joint_count,), UACJointFF), (False, None)
			yield 'pc_floats', Array, (0, None, (instance.pc_count, 10,), Float), (False, None)
		yield 'joint_to_bone', Array, (0, None, (instance.joint_count,), Int), (False, None)
		yield 'bone_to_joint', Array, (0, None, (instance.bone_count,), Int), (False, None)
		yield 'joint_names', ZStringBuffer, (instance.namespace_length, None), (False, None)
		if instance.context.version >= 47:
			yield 'joint_names_padding', PadAlign, (8, instance.names_ref), (False, None)
		if instance.context.version <= 32:
			yield 'joint_names_padding', SmartPadding, (0, None), (False, None)
		if instance.context.version >= 47:
			yield 'joint_infos', Array, (instance.joint_names, None, (instance.joint_count,), JointInfo), (False, None)
		if instance.context.version <= 32:
			yield 'hitcheck_reader', HitcheckReader, (instance, None), (False, None)

	def get_strings(self):
		"""Get all strings in the structure."""
		condition_function = lambda x: issubclass(x[1], OffsetString)
		for val in self.get_condition_values_recursive(self, condition_function):
			yield val

	def get_pointers(self):
		"""Get all strings in the structure."""
		condition_function = lambda x: issubclass(x[1], JointPointer)
		for val in self.get_condition_values_recursive(self, condition_function):
			yield val

	def get_string_attribs(self):
		"""Get all strings in the structure."""
		condition_function = lambda x: issubclass(x[1], OffsetString)
		for s_type, s_inst, (f_name, f_type, arguments, _) in self.get_condition_attributes_recursive(self, self, condition_function):
			yield s_inst, f_name

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		# after reading, we can resolve the joint pointers
		for ptr in instance.get_pointers():
			ptr.joint = instance.joint_infos[ptr.index]
	# 	# after reading, resolve the names to string
	# 	for child_instance, attrib in instance.get_string_attribs():
	# 		# get the offset
	# 		offset = child_instance.get_field(child_instance, attrib)
	# 		# get str from ZStringBuffer
	# 		string = instance.joint_names.get_str_at(offset)
	# 		# set the string
	# 		cls.set_field(child_instance, attrib, string)

	@classmethod
	def write_fields(cls, stream, instance):
		strings = list(instance.get_strings())
		instance.joint_names.update_strings(strings)
		instance.namespace_length = len(instance.joint_names.data)
		# update indices of joint pointers
		joints_map = {j: i for i, j in enumerate(instance.joint_infos)}
		for ptr in instance.get_pointers():
			ptr.index = joints_map.get(ptr.joint)
		super().write_fields(stream, instance)



JointData.init_attributes()
