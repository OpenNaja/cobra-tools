import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Int
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.compounds.ZStringBuffer import ZStringBuffer
from generated.formats.ms2.compounds.HitcheckReader import HitcheckReader
from generated.formats.ms2.compounds.JointEntry import JointEntry
from generated.formats.ms2.compounds.JointInfo import JointInfo
from generated.formats.ms2.compounds.ListCEntry import ListCEntry
from generated.formats.ms2.compounds.ListFirst import ListFirst
from generated.formats.ms2.compounds.ListLong import ListLong
from generated.formats.ms2.compounds.ListShort import ListShort
from generated.formats.ms2.compounds.UACJointFF import UACJointFF
from generated.formats.ovl_base.compounds.SmartPadding import SmartPadding


class JointData(BaseStruct):

	"""
	appears in dinos and static meshes
	"""

	__name__ = 'JointData'

	_import_path = 'generated.formats.ms2.compounds.JointData'

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

		# corresponds to bone transforms
		self.joint_transforms = Array(self.context, 0, None, (0,), JointEntry)

		# might be pointers
		self.zeros_3 = Array(self.context, 0, None, (0,), Uint64)

		# ?
		self.unknown_listc = Array(self.context, 0, None, (0,), ListCEntry)

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

		# ?
		self.joint_names_padding = SmartPadding(self.context, 0, None)

		# new style - includes name offset, some flags and the hitchecks
		self.joint_infos = Array(self.context, 0, None, (0,), JointInfo)

		# old style - for each joint, read the hitchecks
		self.hitcheck_reader = HitcheckReader(self.context, self.joint_infos, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		if self.context.version == 32:
			self.start_pc = SmartPadding(self.context, 0, None)
		if self.context.version <= 7:
			self.before_dla_0 = 0
			self.before_dla_1 = 0
		self.joint_count = 0
		self.count_0 = 0
		self.count_1 = 0
		self.count_2 = 0
		if self.context.version <= 32:
			self.zero_0 = 0
		if 13 <= self.context.version <= 32:
			self.zero_1 = 0
		self.namespace_length = 0
		self.zeros_0 = numpy.zeros((5,), dtype=numpy.dtype('uint32'))
		self.pc_count = 0
		self.zeros_1 = numpy.zeros((7,), dtype=numpy.dtype('uint32'))
		if 13 <= self.context.version <= 32:
			self.extra_zeros_2 = numpy.zeros((4,), dtype=numpy.dtype('uint32'))
		if self.context.version >= 13:
			self.ones = numpy.zeros((2,), dtype=numpy.dtype('uint64'))
		self.bone_count = 0
		self.joint_entry_count = 0
		self.zeros_2 = numpy.zeros((4,), dtype=numpy.dtype('uint32'))
		if self.context.version <= 7:
			self.zeros_3 = 0
		self.joint_transforms = Array(self.context, 0, None, (self.joint_count,), JointEntry)
		if self.context.version >= 47:
			self.zeros_3 = numpy.zeros((self.joint_count,), dtype=numpy.dtype('uint64'))
			self.unknown_listc = Array(self.context, 0, None, (self.joint_count,), ListCEntry)
			self.first_list = Array(self.context, 0, None, (self.count_0,), ListFirst)
			self.short_list = Array(self.context, 0, None, (self.count_1,), ListShort)
			self.long_list = Array(self.context, 0, None, (self.count_2,), ListLong)
		if self.context.version <= 32:
			self.joint_infos = Array(self.context, 0, None, (self.joint_count,), UACJointFF)
			self.pc_floats = numpy.zeros((self.pc_count, 10,), dtype=numpy.dtype('float32'))
		self.joint_indices = numpy.zeros((self.joint_count,), dtype=numpy.dtype('int32'))
		self.bone_indices = numpy.zeros((self.bone_count,), dtype=numpy.dtype('int32'))
		self.joint_names = ZStringBuffer(self.context, self.namespace_length, None)
		self.joint_names_padding = SmartPadding(self.context, 0, None)
		if self.context.version >= 47:
			self.joint_infos = Array(self.context, 0, None, (self.joint_count,), JointInfo)
		if self.context.version <= 32:
			self.hitcheck_reader = HitcheckReader(self.context, self.joint_infos, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		if instance.context.version == 32:
			instance.start_pc = SmartPadding.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 7:
			instance.before_dla_0 = Uint64.from_stream(stream, instance.context, 0, None)
			instance.before_dla_1 = Uint64.from_stream(stream, instance.context, 0, None)
		instance.joint_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.count_0 = Uint.from_stream(stream, instance.context, 0, None)
		instance.count_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.count_2 = Uint.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 32:
			instance.zero_0 = Uint.from_stream(stream, instance.context, 0, None)
		if 13 <= instance.context.version <= 32:
			instance.zero_1 = Uint.from_stream(stream, instance.context, 0, None)
		instance.namespace_length = Uint.from_stream(stream, instance.context, 0, None)
		instance.zeros_0 = Array.from_stream(stream, instance.context, 0, None, (5,), Uint)
		instance.pc_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.zeros_1 = Array.from_stream(stream, instance.context, 0, None, (7,), Uint)
		if 13 <= instance.context.version <= 32:
			instance.extra_zeros_2 = Array.from_stream(stream, instance.context, 0, None, (4,), Uint)
		if instance.context.version >= 13:
			instance.ones = Array.from_stream(stream, instance.context, 0, None, (2,), Uint64)
		instance.bone_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.joint_entry_count = Uint.from_stream(stream, instance.context, 0, None)
		instance.zeros_2 = Array.from_stream(stream, instance.context, 0, None, (4,), Uint)
		if instance.context.version <= 7:
			instance.zeros_3 = Uint.from_stream(stream, instance.context, 0, None)
		instance.joint_transforms = Array.from_stream(stream, instance.context, 0, None, (instance.joint_count,), JointEntry)
		if instance.context.version >= 47:
			instance.zeros_3 = Array.from_stream(stream, instance.context, 0, None, (instance.joint_count,), Uint64)
			instance.unknown_listc = Array.from_stream(stream, instance.context, 0, None, (instance.joint_count,), ListCEntry)
			instance.first_list = Array.from_stream(stream, instance.context, 0, None, (instance.count_0,), ListFirst)
			instance.short_list = Array.from_stream(stream, instance.context, 0, None, (instance.count_1,), ListShort)
			instance.long_list = Array.from_stream(stream, instance.context, 0, None, (instance.count_2,), ListLong)
		if instance.context.version <= 32:
			instance.joint_infos = Array.from_stream(stream, instance.context, 0, None, (instance.joint_count,), UACJointFF)
			instance.pc_floats = Array.from_stream(stream, instance.context, 0, None, (instance.pc_count, 10,), Float)
		instance.joint_indices = Array.from_stream(stream, instance.context, 0, None, (instance.joint_count,), Int)
		instance.bone_indices = Array.from_stream(stream, instance.context, 0, None, (instance.bone_count,), Int)
		instance.joint_names = ZStringBuffer.from_stream(stream, instance.context, instance.namespace_length, None)
		instance.joint_names_padding = SmartPadding.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 47:
			instance.joint_infos = Array.from_stream(stream, instance.context, 0, None, (instance.joint_count,), JointInfo)
		if instance.context.version <= 32:
			instance.hitcheck_reader = HitcheckReader.from_stream(stream, instance.context, instance.joint_infos, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.context.version == 32:
			SmartPadding.to_stream(stream, instance.start_pc)
		if instance.context.version <= 7:
			Uint64.to_stream(stream, instance.before_dla_0)
			Uint64.to_stream(stream, instance.before_dla_1)
		Uint.to_stream(stream, instance.joint_count)
		Uint.to_stream(stream, instance.count_0)
		Uint.to_stream(stream, instance.count_1)
		Uint.to_stream(stream, instance.count_2)
		if instance.context.version <= 32:
			Uint.to_stream(stream, instance.zero_0)
		if 13 <= instance.context.version <= 32:
			Uint.to_stream(stream, instance.zero_1)
		Uint.to_stream(stream, instance.namespace_length)
		Array.to_stream(stream, instance.zeros_0, Uint)
		Uint.to_stream(stream, instance.pc_count)
		Array.to_stream(stream, instance.zeros_1, Uint)
		if 13 <= instance.context.version <= 32:
			Array.to_stream(stream, instance.extra_zeros_2, Uint)
		if instance.context.version >= 13:
			Array.to_stream(stream, instance.ones, Uint64)
		Uint.to_stream(stream, instance.bone_count)
		Uint.to_stream(stream, instance.joint_entry_count)
		Array.to_stream(stream, instance.zeros_2, Uint)
		if instance.context.version <= 7:
			Uint.to_stream(stream, instance.zeros_3)
		Array.to_stream(stream, instance.joint_transforms, JointEntry)
		if instance.context.version >= 47:
			Array.to_stream(stream, instance.zeros_3, Uint64)
			Array.to_stream(stream, instance.unknown_listc, ListCEntry)
			Array.to_stream(stream, instance.first_list, ListFirst)
			Array.to_stream(stream, instance.short_list, ListShort)
			Array.to_stream(stream, instance.long_list, ListLong)
		if instance.context.version <= 32:
			Array.to_stream(stream, instance.joint_infos, UACJointFF)
			Array.to_stream(stream, instance.pc_floats, Float)
		Array.to_stream(stream, instance.joint_indices, Int)
		Array.to_stream(stream, instance.bone_indices, Int)
		ZStringBuffer.to_stream(stream, instance.joint_names)
		SmartPadding.to_stream(stream, instance.joint_names_padding)
		if instance.context.version >= 47:
			Array.to_stream(stream, instance.joint_infos, JointInfo)
		if instance.context.version <= 32:
			HitcheckReader.to_stream(stream, instance.hitcheck_reader)

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
		yield 'joint_transforms', Array, (0, None, (instance.joint_count,), JointEntry), (False, None)
		if instance.context.version >= 47:
			yield 'zeros_3', Array, (0, None, (instance.joint_count,), Uint64), (False, None)
			yield 'unknown_listc', Array, (0, None, (instance.joint_count,), ListCEntry), (False, None)
			yield 'first_list', Array, (0, None, (instance.count_0,), ListFirst), (False, None)
			yield 'short_list', Array, (0, None, (instance.count_1,), ListShort), (False, None)
			yield 'long_list', Array, (0, None, (instance.count_2,), ListLong), (False, None)
		if instance.context.version <= 32:
			yield 'joint_infos', Array, (0, None, (instance.joint_count,), UACJointFF), (False, None)
			yield 'pc_floats', Array, (0, None, (instance.pc_count, 10,), Float), (False, None)
		yield 'joint_indices', Array, (0, None, (instance.joint_count,), Int), (False, None)
		yield 'bone_indices', Array, (0, None, (instance.bone_count,), Int), (False, None)
		yield 'joint_names', ZStringBuffer, (instance.namespace_length, None), (False, None)
		yield 'joint_names_padding', SmartPadding, (0, None), (False, None)
		if instance.context.version >= 47:
			yield 'joint_infos', Array, (0, None, (instance.joint_count,), JointInfo), (False, None)
		if instance.context.version <= 32:
			yield 'hitcheck_reader', HitcheckReader, (instance.joint_infos, None), (False, None)

	def get_info_str(self, indent=0):
		return f'JointData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
