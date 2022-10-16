from generated.base_struct import BaseStruct
from generated.formats.ms2.basic import OffsetString
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
from generated.formats.ms2.compounds.JointEntry import JointEntry
from generated.formats.ms2.compounds.JointInfo import JointInfo
from generated.formats.ms2.compounds.ListFirst import ListFirst
from generated.formats.ms2.compounds.ListLong import ListLong
from generated.formats.ms2.compounds.ListShort import ListShort
from generated.formats.ms2.compounds.RigidBody import RigidBody
from generated.formats.ms2.compounds.UACJointFF import UACJointFF
from generated.formats.ovl_base.compounds.Empty import Empty
from generated.formats.ovl_base.compounds.SmartPadding import SmartPadding


class JointData(BaseStruct):

	"""
	appears in dinos and static meshes
	"""

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
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
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

		# 1, 1
		self.ones = Array(self.context, 0, None, (0,), Uint64)

		# matches bone count from bone info
		self.bone_count = 0

		# 0
		self.joint_entry_count = 0

		# usually 0s
		self.zeros_2 = Array(self.context, 0, None, (0,), Uint)

		# usually 0s
		self.zeros_3 = 0
		self.names_ref = Empty(self.context, 0, None)

		# corresponds to bone transforms
		self.joint_transforms = Array(self.context, 0, None, (0,), JointEntry)
		self.rigid_body_pointers = Array(self.context, 0, None, (0,), Uint64)
		self.rigid_body_list = Array(self.context, 0, None, (0,), RigidBody)

		# used by ptero, 16 bytes per entry
		self.first_list = Array(self.context, 0, None, (0,), ListFirst)

		# ?
		self.short_list = Array(self.context, 0, None, (0,), ListShort)

		# ?
		self.long_list = Array(self.context, 0, None, (0,), ListLong)

		# old style - joint infos, without hitchecks, they are added later
		self.joint_infos = Array(self.context, 0, None, (0,), UACJointFF)

		# sometimes an array of floats
		self.pc_floats = Array(self.context, 0, None, (0,), Float)

		# index into bone info bones for each joint; bone that the joint is attached to
		self.joint_indices = Array(self.context, 0, None, (0,), Int)

		# the inverse of the above; for each bone info bone, index of the corresponding joint or -1 if no joint
		self.bone_indices = Array(self.context, 0, None, (0,), Int)

		# zstring name buffer
		self.joint_names = ZStringBuffer(self.context, self.namespace_length, None)

		# align to 4

		# ?
		self.joint_names_padding = SmartPadding(self.context, 0, None)

		# new style - includes name offset, some flags and the hitchecks
		self.joint_infos = Array(self.context, self.joint_names, None, (0,), JointInfo)

		# old style - for each joint, read the hitchecks
		self.hitcheck_reader = HitcheckReader(self.context, self, None)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('start_pc', SmartPadding, (0, None), (False, None), True),
		('before_dla_0', Uint64, (0, None), (False, None), True),
		('before_dla_1', Uint64, (0, None), (False, None), True),
		('joint_count', Uint, (0, None), (False, None), None),
		('count_0', Uint, (0, None), (False, None), None),
		('count_1', Uint, (0, None), (False, None), None),
		('count_2', Uint, (0, None), (False, None), None),
		('zero_0', Uint, (0, None), (False, None), True),
		('zero_1', Uint, (0, None), (False, None), True),
		('namespace_length', Uint, (0, None), (False, None), None),
		('zeros_0', Array, (0, None, (5,), Uint), (False, None), None),
		('pc_count', Uint, (0, None), (False, None), None),
		('zeros_1', Array, (0, None, (7,), Uint), (False, None), None),
		('extra_zeros_2', Array, (0, None, (4,), Uint), (False, None), True),
		('ones', Array, (0, None, (2,), Uint64), (False, None), True),
		('bone_count', Uint, (0, None), (False, None), None),
		('joint_entry_count', Uint, (0, None), (False, None), None),
		('zeros_2', Array, (0, None, (4,), Uint), (False, None), None),
		('zeros_3', Uint, (0, None), (False, None), True),
		('names_ref', Empty, (0, None), (False, None), None),
		('joint_transforms', Array, (0, None, (None,), JointEntry), (False, None), None),
		('rigid_body_pointers', Array, (0, None, (None,), Uint64), (False, None), True),
		('rigid_body_list', Array, (0, None, (None,), RigidBody), (False, None), True),
		('first_list', Array, (0, None, (None,), ListFirst), (False, None), True),
		('short_list', Array, (0, None, (None,), ListShort), (False, None), True),
		('long_list', Array, (0, None, (None,), ListLong), (False, None), True),
		('joint_infos', Array, (0, None, (None,), UACJointFF), (False, None), True),
		('pc_floats', Array, (0, None, (None, 10,), Float), (False, None), True),
		('joint_indices', Array, (0, None, (None,), Int), (False, None), None),
		('bone_indices', Array, (0, None, (None,), Int), (False, None), None),
		('joint_names', ZStringBuffer, (None, None), (False, None), None),
		('joint_names_padding', PadAlign, (8, None), (False, None), True),
		('joint_names_padding', SmartPadding, (0, None), (False, None), True),
		('joint_infos', Array, (None, None, (None,), JointInfo), (False, None), True),
		('hitcheck_reader', HitcheckReader, (None, None), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version == 32:
			yield 'start_pc', SmartPadding, (0, None), (False, None)
		if instance.context.version <= 7:
			yield 'before_dla_0', Uint64, (0, None), (False, None)
			yield 'before_dla_1', Uint64, (0, None), (False, None)
		yield 'joint_count', Uint, (0, None), (False, None)
		yield 'count_0', Uint, (0, None), (False, None)
		yield 'count_1', Uint, (0, None), (False, None)
		yield 'count_2', Uint, (0, None), (False, None)
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
			yield 'ones', Array, (0, None, (2,), Uint64), (False, None)
		yield 'bone_count', Uint, (0, None), (False, None)
		yield 'joint_entry_count', Uint, (0, None), (False, None)
		yield 'zeros_2', Array, (0, None, (4,), Uint), (False, None)
		if instance.context.version <= 7:
			yield 'zeros_3', Uint, (0, None), (False, None)
		yield 'names_ref', Empty, (0, None), (False, None)
		yield 'joint_transforms', Array, (0, None, (instance.joint_count,), JointEntry), (False, None)
		if instance.context.version >= 47:
			yield 'rigid_body_pointers', Array, (0, None, (instance.joint_count,), Uint64), (False, None)
			yield 'rigid_body_list', Array, (0, None, (instance.joint_count,), RigidBody), (False, None)
			yield 'first_list', Array, (0, None, (instance.count_0,), ListFirst), (False, None)
			yield 'short_list', Array, (0, None, (instance.count_1,), ListShort), (False, None)
			yield 'long_list', Array, (0, None, (instance.count_2,), ListLong), (False, None)
		if instance.context.version <= 32:
			yield 'joint_infos', Array, (0, None, (instance.joint_count,), UACJointFF), (False, None)
			yield 'pc_floats', Array, (0, None, (instance.pc_count, 10,), Float), (False, None)
		yield 'joint_indices', Array, (0, None, (instance.joint_count,), Int), (False, None)
		yield 'bone_indices', Array, (0, None, (instance.bone_count,), Int), (False, None)
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
			logging.info(val)
			yield val

	def get_string_attribs(self):
		"""Get all strings in the structure."""
		condition_function = lambda x: issubclass(x[1], OffsetString)
		for s_type, s_inst, (f_name, f_type, arguments, _) in self.get_condition_attributes_recursive(self, self, condition_function):
			yield s_inst, f_name

	# @classmethod
	# def read_fields(cls, stream, instance):
	# 	super().read_fields(stream, instance)
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
		logging.info(strings)
		instance.joint_names.update_strings(strings)
		instance.namespace_length = len(instance.joint_names.data)
		super().write_fields(stream, instance)

