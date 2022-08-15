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
		self.zeros_0 = numpy.zeros((5,), dtype=numpy.dtype('uint32'))

		# 0 or 1
		self.pc_count = 0

		# 0s
		self.zeros_1 = numpy.zeros((7,), dtype=numpy.dtype('uint32'))

		# 0s
		self.extra_zeros_2 = numpy.zeros((4,), dtype=numpy.dtype('uint32'))

		# 1, 1
		self.ones = numpy.zeros((2,), dtype=numpy.dtype('uint64'))

		# matches bone count from bone info
		self.bone_count = 0

		# 0
		self.joint_entry_count = 0

		# usually 0s
		self.zeros_2 = numpy.zeros((4,), dtype=numpy.dtype('uint32'))

		# usually 0s
		self.zeros_3 = 0

		# corresponds to bone transforms
		self.joint_transforms = Array((self.joint_count,), JointEntry, self.context, 0, None)

		# might be pointers
		self.zeros_3 = numpy.zeros((self.joint_count,), dtype=numpy.dtype('uint64'))

		# ?
		self.unknown_listc = Array((self.joint_count,), ListCEntry, self.context, 0, None)

		# used by ptero, 16 bytes per entry
		self.first_list = Array((self.count_0,), ListFirst, self.context, 0, None)

		# ?
		self.short_list = Array((self.count_1,), ListShort, self.context, 0, None)

		# ?
		self.long_list = Array((self.count_2,), ListLong, self.context, 0, None)

		# old style - joint infos, without hitchecks, they are added later
		self.joint_infos = Array((self.joint_count,), UACJointFF, self.context, 0, None)

		# sometimes an array of floats
		self.pc_floats = numpy.zeros((self.pc_count, 10,), dtype=numpy.dtype('float32'))

		# index into bone info bones for each joint; bone that the joint is attached to
		self.joint_indices = numpy.zeros((self.joint_count,), dtype=numpy.dtype('int32'))

		# the inverse of the above; for each bone info bone, index of the corresponding joint or -1 if no joint
		self.bone_indices = numpy.zeros((self.bone_count,), dtype=numpy.dtype('int32'))

		# zstring name buffer
		self.joint_names = ZStringBuffer(self.context, self.namespace_length, None)

		# ?
		self.joint_names_padding = SmartPadding(self.context, 0, None)

		# new style - includes name offset, some flags and the hitchecks
		self.joint_infos = Array((self.joint_count,), JointInfo, self.context, 0, None)

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
		self.joint_transforms = Array((self.joint_count,), JointEntry, self.context, 0, None)
		if self.context.version >= 47:
			self.zeros_3 = numpy.zeros((self.joint_count,), dtype=numpy.dtype('uint64'))
			self.unknown_listc = Array((self.joint_count,), ListCEntry, self.context, 0, None)
			self.first_list = Array((self.count_0,), ListFirst, self.context, 0, None)
			self.short_list = Array((self.count_1,), ListShort, self.context, 0, None)
			self.long_list = Array((self.count_2,), ListLong, self.context, 0, None)
		if self.context.version <= 32:
			self.joint_infos = Array((self.joint_count,), UACJointFF, self.context, 0, None)
			self.pc_floats = numpy.zeros((self.pc_count, 10,), dtype=numpy.dtype('float32'))
		self.joint_indices = numpy.zeros((self.joint_count,), dtype=numpy.dtype('int32'))
		self.bone_indices = numpy.zeros((self.bone_count,), dtype=numpy.dtype('int32'))
		self.joint_names = ZStringBuffer(self.context, self.namespace_length, None)
		self.joint_names_padding = SmartPadding(self.context, 0, None)
		if self.context.version >= 47:
			self.joint_infos = Array((self.joint_count,), JointInfo, self.context, 0, None)
		if self.context.version <= 32:
			self.hitcheck_reader = HitcheckReader(self.context, self.joint_infos, None)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		if instance.context.version == 32:
			instance.start_pc = SmartPadding.from_stream(stream, instance.context, 0, None)
		if instance.context.version <= 7:
			instance.before_dla_0 = stream.read_uint64()
			instance.before_dla_1 = stream.read_uint64()
		instance.joint_count = stream.read_uint()
		instance.count_0 = stream.read_uint()
		instance.count_1 = stream.read_uint()
		instance.count_2 = stream.read_uint()
		if instance.context.version <= 32:
			instance.zero_0 = stream.read_uint()
		if 13 <= instance.context.version <= 32:
			instance.zero_1 = stream.read_uint()
		instance.namespace_length = stream.read_uint()
		instance.zeros_0 = stream.read_uints((5,))
		instance.pc_count = stream.read_uint()
		instance.zeros_1 = stream.read_uints((7,))
		if 13 <= instance.context.version <= 32:
			instance.extra_zeros_2 = stream.read_uints((4,))
		if instance.context.version >= 13:
			instance.ones = stream.read_uint64s((2,))
		instance.bone_count = stream.read_uint()
		instance.joint_entry_count = stream.read_uint()
		instance.zeros_2 = stream.read_uints((4,))
		if instance.context.version <= 7:
			instance.zeros_3 = stream.read_uint()
		instance.joint_transforms = Array.from_stream(stream, (instance.joint_count,), JointEntry, instance.context, 0, None)
		if instance.context.version >= 47:
			instance.zeros_3 = stream.read_uint64s((instance.joint_count,))
			instance.unknown_listc = Array.from_stream(stream, (instance.joint_count,), ListCEntry, instance.context, 0, None)
			instance.first_list = Array.from_stream(stream, (instance.count_0,), ListFirst, instance.context, 0, None)
			instance.short_list = Array.from_stream(stream, (instance.count_1,), ListShort, instance.context, 0, None)
			instance.long_list = Array.from_stream(stream, (instance.count_2,), ListLong, instance.context, 0, None)
		if instance.context.version <= 32:
			instance.joint_infos = Array.from_stream(stream, (instance.joint_count,), UACJointFF, instance.context, 0, None)
			instance.pc_floats = stream.read_floats((instance.pc_count, 10,))
		instance.joint_indices = stream.read_ints((instance.joint_count,))
		instance.bone_indices = stream.read_ints((instance.bone_count,))
		instance.joint_names = ZStringBuffer.from_stream(stream, instance.context, instance.namespace_length, None)
		instance.joint_names_padding = SmartPadding.from_stream(stream, instance.context, 0, None)
		if instance.context.version >= 47:
			instance.joint_infos = Array.from_stream(stream, (instance.joint_count,), JointInfo, instance.context, 0, None)
		if instance.context.version <= 32:
			instance.hitcheck_reader = HitcheckReader.from_stream(stream, instance.context, instance.joint_infos, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		if instance.context.version == 32:
			SmartPadding.to_stream(stream, instance.start_pc)
		if instance.context.version <= 7:
			stream.write_uint64(instance.before_dla_0)
			stream.write_uint64(instance.before_dla_1)
		stream.write_uint(instance.joint_count)
		stream.write_uint(instance.count_0)
		stream.write_uint(instance.count_1)
		stream.write_uint(instance.count_2)
		if instance.context.version <= 32:
			stream.write_uint(instance.zero_0)
		if 13 <= instance.context.version <= 32:
			stream.write_uint(instance.zero_1)
		stream.write_uint(instance.namespace_length)
		stream.write_uints(instance.zeros_0)
		stream.write_uint(instance.pc_count)
		stream.write_uints(instance.zeros_1)
		if 13 <= instance.context.version <= 32:
			stream.write_uints(instance.extra_zeros_2)
		if instance.context.version >= 13:
			stream.write_uint64s(instance.ones)
		stream.write_uint(instance.bone_count)
		stream.write_uint(instance.joint_entry_count)
		stream.write_uints(instance.zeros_2)
		if instance.context.version <= 7:
			stream.write_uint(instance.zeros_3)
		Array.to_stream(stream, instance.joint_transforms, (instance.joint_count,), JointEntry, instance.context, 0, None)
		if instance.context.version >= 47:
			stream.write_uint64s(instance.zeros_3)
			Array.to_stream(stream, instance.unknown_listc, (instance.joint_count,), ListCEntry, instance.context, 0, None)
			Array.to_stream(stream, instance.first_list, (instance.count_0,), ListFirst, instance.context, 0, None)
			Array.to_stream(stream, instance.short_list, (instance.count_1,), ListShort, instance.context, 0, None)
			Array.to_stream(stream, instance.long_list, (instance.count_2,), ListLong, instance.context, 0, None)
		if instance.context.version <= 32:
			Array.to_stream(stream, instance.joint_infos, (instance.joint_count,), UACJointFF, instance.context, 0, None)
			stream.write_floats(instance.pc_floats)
		stream.write_ints(instance.joint_indices)
		stream.write_ints(instance.bone_indices)
		ZStringBuffer.to_stream(stream, instance.joint_names)
		SmartPadding.to_stream(stream, instance.joint_names_padding)
		if instance.context.version >= 47:
			Array.to_stream(stream, instance.joint_infos, (instance.joint_count,), JointInfo, instance.context, 0, None)
		if instance.context.version <= 32:
			HitcheckReader.to_stream(stream, instance.hitcheck_reader)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		if instance.context.version == 32:
			yield 'start_pc', SmartPadding, (0, None)
		if instance.context.version <= 7:
			yield 'before_dla_0', Uint64, (0, None)
			yield 'before_dla_1', Uint64, (0, None)
		yield 'joint_count', Uint, (0, None)
		yield 'count_0', Uint, (0, None)
		yield 'count_1', Uint, (0, None)
		yield 'count_2', Uint, (0, None)
		if instance.context.version <= 32:
			yield 'zero_0', Uint, (0, None)
		if 13 <= instance.context.version <= 32:
			yield 'zero_1', Uint, (0, None)
		yield 'namespace_length', Uint, (0, None)
		yield 'zeros_0', Array, ((5,), Uint, 0, None)
		yield 'pc_count', Uint, (0, None)
		yield 'zeros_1', Array, ((7,), Uint, 0, None)
		if 13 <= instance.context.version <= 32:
			yield 'extra_zeros_2', Array, ((4,), Uint, 0, None)
		if instance.context.version >= 13:
			yield 'ones', Array, ((2,), Uint64, 0, None)
		yield 'bone_count', Uint, (0, None)
		yield 'joint_entry_count', Uint, (0, None)
		yield 'zeros_2', Array, ((4,), Uint, 0, None)
		if instance.context.version <= 7:
			yield 'zeros_3', Uint, (0, None)
		yield 'joint_transforms', Array, ((instance.joint_count,), JointEntry, 0, None)
		if instance.context.version >= 47:
			yield 'zeros_3', Array, ((instance.joint_count,), Uint64, 0, None)
			yield 'unknown_listc', Array, ((instance.joint_count,), ListCEntry, 0, None)
			yield 'first_list', Array, ((instance.count_0,), ListFirst, 0, None)
			yield 'short_list', Array, ((instance.count_1,), ListShort, 0, None)
			yield 'long_list', Array, ((instance.count_2,), ListLong, 0, None)
		if instance.context.version <= 32:
			yield 'joint_infos', Array, ((instance.joint_count,), UACJointFF, 0, None)
			yield 'pc_floats', Array, ((instance.pc_count, 10,), Float, 0, None)
		yield 'joint_indices', Array, ((instance.joint_count,), Int, 0, None)
		yield 'bone_indices', Array, ((instance.bone_count,), Int, 0, None)
		yield 'joint_names', ZStringBuffer, (instance.namespace_length, None)
		yield 'joint_names_padding', SmartPadding, (0, None)
		if instance.context.version >= 47:
			yield 'joint_infos', Array, ((instance.joint_count,), JointInfo, 0, None)
		if instance.context.version <= 32:
			yield 'hitcheck_reader', HitcheckReader, (instance.joint_infos, None)

	def get_info_str(self, indent=0):
		return f'JointData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* start_pc = {self.fmt_member(self.start_pc, indent+1)}'
		s += f'\n	* before_dla_0 = {self.fmt_member(self.before_dla_0, indent+1)}'
		s += f'\n	* before_dla_1 = {self.fmt_member(self.before_dla_1, indent+1)}'
		s += f'\n	* joint_count = {self.fmt_member(self.joint_count, indent+1)}'
		s += f'\n	* count_0 = {self.fmt_member(self.count_0, indent+1)}'
		s += f'\n	* count_1 = {self.fmt_member(self.count_1, indent+1)}'
		s += f'\n	* count_2 = {self.fmt_member(self.count_2, indent+1)}'
		s += f'\n	* zero_0 = {self.fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* zero_1 = {self.fmt_member(self.zero_1, indent+1)}'
		s += f'\n	* namespace_length = {self.fmt_member(self.namespace_length, indent+1)}'
		s += f'\n	* zeros_0 = {self.fmt_member(self.zeros_0, indent+1)}'
		s += f'\n	* pc_count = {self.fmt_member(self.pc_count, indent+1)}'
		s += f'\n	* zeros_1 = {self.fmt_member(self.zeros_1, indent+1)}'
		s += f'\n	* extra_zeros_2 = {self.fmt_member(self.extra_zeros_2, indent+1)}'
		s += f'\n	* ones = {self.fmt_member(self.ones, indent+1)}'
		s += f'\n	* bone_count = {self.fmt_member(self.bone_count, indent+1)}'
		s += f'\n	* joint_entry_count = {self.fmt_member(self.joint_entry_count, indent+1)}'
		s += f'\n	* zeros_2 = {self.fmt_member(self.zeros_2, indent+1)}'
		s += f'\n	* zeros_3 = {self.fmt_member(self.zeros_3, indent+1)}'
		s += f'\n	* joint_transforms = {self.fmt_member(self.joint_transforms, indent+1)}'
		s += f'\n	* zeros_3 = {self.fmt_member(self.zeros_3, indent+1)}'
		s += f'\n	* unknown_listc = {self.fmt_member(self.unknown_listc, indent+1)}'
		s += f'\n	* first_list = {self.fmt_member(self.first_list, indent+1)}'
		s += f'\n	* short_list = {self.fmt_member(self.short_list, indent+1)}'
		s += f'\n	* long_list = {self.fmt_member(self.long_list, indent+1)}'
		s += f'\n	* joint_infos = {self.fmt_member(self.joint_infos, indent+1)}'
		s += f'\n	* pc_floats = {self.fmt_member(self.pc_floats, indent+1)}'
		s += f'\n	* joint_indices = {self.fmt_member(self.joint_indices, indent+1)}'
		s += f'\n	* bone_indices = {self.fmt_member(self.bone_indices, indent+1)}'
		s += f'\n	* joint_names = {self.fmt_member(self.joint_names, indent+1)}'
		s += f'\n	* joint_names_padding = {self.fmt_member(self.joint_names_padding, indent+1)}'
		s += f'\n	* joint_infos = {self.fmt_member(self.joint_infos, indent+1)}'
		s += f'\n	* hitcheck_reader = {self.fmt_member(self.hitcheck_reader, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
