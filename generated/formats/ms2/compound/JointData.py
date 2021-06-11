import numpy
import typing
from generated.array import Array
from generated.formats.ms2.compound.HitCheckEntry import HitCheckEntry
from generated.formats.ms2.compound.JointEntry import JointEntry
from generated.formats.ms2.compound.JointInfo import JointInfo
from generated.formats.ms2.compound.ListCEntry import ListCEntry
from generated.formats.ms2.compound.ListFirst import ListFirst
from generated.formats.ms2.compound.ListLong import ListLong
from generated.formats.ms2.compound.ListShort import ListShort
from generated.formats.ms2.compound.PcFFCounter import PcFFCounter
from generated.formats.ms2.compound.SmartPadding import SmartPadding
from generated.formats.ms2.compound.ZStringBuffer import ZStringBuffer


class JointData:

	"""
	appears in dinos and static meshes
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# repeat
		self.joint_count = 0

		# small number
		self.count_0 = 0

		# small number
		self.count_1 = 0

		# small number
		self.count_2 = 0

		# 0s, might be related to count 7 in PC
		self.zeros_extra = numpy.zeros((2), dtype='uint')
		self.namespace_length = 0

		# 0s
		self.zeros_0 = numpy.zeros((5), dtype='uint')

		# 0 or 1
		self.pc_count = 0

		# 0s
		self.zeros_1 = numpy.zeros((7), dtype='uint')

		# 0s
		self.extra_zeros_pc = numpy.zeros((4), dtype='uint')

		# 1, 1
		self.ones = numpy.zeros((2), dtype='uint64')

		# matches bone count from bone info
		self.bone_count = 0

		# 0
		self.joint_entry_count = 0

		# usually 0s
		self.zeros_2 = numpy.zeros((4), dtype='uint')

		# corresponds to bone transforms
		self.joint_transforms = Array()

		# might be pointers
		self.zeros_3 = numpy.zeros((self.joint_count), dtype='uint64')
		self.unknown_listc = Array()

		# used by ptero, 16 bytes per entry
		self.first_list = Array()
		self.short_list = Array()
		self.long_list = Array()
		self.pc_ffs = PcFFCounter()

		# 1FAA FFAAFF00 000000
		self.pc_bytes = numpy.zeros((9), dtype='byte')

		# some count, not sure if used
		self.pc_hitcheck_count = 0

		# 0
		self.pc_zero_0 = 0

		# sometimes an array of floats
		self.pc_floats = numpy.zeros((self.pc_count, 10), dtype='float')

		# index into bone info bones for each joint; bone that the joint is attached to
		self.joint_indices = numpy.zeros((self.joint_count), dtype='int')

		# the inverse of the above; for each bone info bone, index of the corresponding joint or -1 if no joint
		self.bone_indices = numpy.zeros((self.bone_count), dtype='int')
		self.joint_names = ZStringBuffer()
		self.joint_names_padding = SmartPadding()
		self.joint_info_list = Array()
		self.hitchecks_pc = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.joint_count = stream.read_uint()
		self.count_0 = stream.read_uint()
		self.count_1 = stream.read_uint()
		self.count_2 = stream.read_uint()
		if stream.version == 18:
			self.zeros_extra = stream.read_uints((2))
		self.namespace_length = stream.read_uint()
		self.zeros_0 = stream.read_uints((5))
		self.pc_count = stream.read_uint()
		self.zeros_1 = stream.read_uints((7))
		if stream.version == 18:
			self.extra_zeros_pc = stream.read_uints((4))
		self.ones = stream.read_uint64s((2))
		self.bone_count = stream.read_uint()
		self.joint_entry_count = stream.read_uint()
		self.zeros_2 = stream.read_uints((4))
		self.joint_transforms.read(stream, JointEntry, self.joint_count, None)
		if not (stream.version == 18):
			self.zeros_3 = stream.read_uint64s((self.joint_count))
			self.unknown_listc.read(stream, ListCEntry, self.joint_count, None)
			self.first_list.read(stream, ListFirst, self.count_0, None)
			self.short_list.read(stream, ListShort, self.count_1, None)
			self.long_list.read(stream, ListLong, self.count_2, None)
		if stream.version == 18:
			self.pc_ffs = stream.read_type(PcFFCounter)
			self.pc_bytes = stream.read_bytes((9))
			self.pc_hitcheck_count = stream.read_uint64()
			self.pc_zero_0 = stream.read_uint64()
			self.pc_floats = stream.read_floats((self.pc_count, 10))
		self.joint_indices = stream.read_ints((self.joint_count))
		self.bone_indices = stream.read_ints((self.bone_count))
		self.joint_names = stream.read_type(ZStringBuffer, (self.namespace_length,))
		self.joint_names_padding = stream.read_type(SmartPadding)
		if not (stream.version == 18):
			self.joint_info_list.read(stream, JointInfo, self.joint_count, None)
		if stream.version == 18:
			self.hitchecks_pc.read(stream, HitCheckEntry, self.pc_hitcheck_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.joint_count)
		stream.write_uint(self.count_0)
		stream.write_uint(self.count_1)
		stream.write_uint(self.count_2)
		if stream.version == 18:
			stream.write_uints(self.zeros_extra)
		stream.write_uint(self.namespace_length)
		stream.write_uints(self.zeros_0)
		stream.write_uint(self.pc_count)
		stream.write_uints(self.zeros_1)
		if stream.version == 18:
			stream.write_uints(self.extra_zeros_pc)
		stream.write_uint64s(self.ones)
		stream.write_uint(self.bone_count)
		stream.write_uint(self.joint_entry_count)
		stream.write_uints(self.zeros_2)
		self.joint_transforms.write(stream, JointEntry, self.joint_count, None)
		if not (stream.version == 18):
			stream.write_uint64s(self.zeros_3)
			self.unknown_listc.write(stream, ListCEntry, self.joint_count, None)
			self.first_list.write(stream, ListFirst, self.count_0, None)
			self.short_list.write(stream, ListShort, self.count_1, None)
			self.long_list.write(stream, ListLong, self.count_2, None)
		if stream.version == 18:
			stream.write_type(self.pc_ffs)
			stream.write_bytes(self.pc_bytes)
			stream.write_uint64(self.pc_hitcheck_count)
			stream.write_uint64(self.pc_zero_0)
			stream.write_floats(self.pc_floats)
		stream.write_ints(self.joint_indices)
		stream.write_ints(self.bone_indices)
		stream.write_type(self.joint_names)
		stream.write_type(self.joint_names_padding)
		if not (stream.version == 18):
			self.joint_info_list.write(stream, JointInfo, self.joint_count, None)
		if stream.version == 18:
			self.hitchecks_pc.write(stream, HitCheckEntry, self.pc_hitcheck_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'JointData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* joint_count = {self.joint_count.__repr__()}'
		s += f'\n	* count_0 = {self.count_0.__repr__()}'
		s += f'\n	* count_1 = {self.count_1.__repr__()}'
		s += f'\n	* count_2 = {self.count_2.__repr__()}'
		s += f'\n	* zeros_extra = {self.zeros_extra.__repr__()}'
		s += f'\n	* namespace_length = {self.namespace_length.__repr__()}'
		s += f'\n	* zeros_0 = {self.zeros_0.__repr__()}'
		s += f'\n	* pc_count = {self.pc_count.__repr__()}'
		s += f'\n	* zeros_1 = {self.zeros_1.__repr__()}'
		s += f'\n	* extra_zeros_pc = {self.extra_zeros_pc.__repr__()}'
		s += f'\n	* ones = {self.ones.__repr__()}'
		s += f'\n	* bone_count = {self.bone_count.__repr__()}'
		s += f'\n	* joint_entry_count = {self.joint_entry_count.__repr__()}'
		s += f'\n	* zeros_2 = {self.zeros_2.__repr__()}'
		s += f'\n	* joint_transforms = {self.joint_transforms.__repr__()}'
		s += f'\n	* zeros_3 = {self.zeros_3.__repr__()}'
		s += f'\n	* unknown_listc = {self.unknown_listc.__repr__()}'
		s += f'\n	* first_list = {self.first_list.__repr__()}'
		s += f'\n	* short_list = {self.short_list.__repr__()}'
		s += f'\n	* long_list = {self.long_list.__repr__()}'
		s += f'\n	* pc_ffs = {self.pc_ffs.__repr__()}'
		s += f'\n	* pc_bytes = {self.pc_bytes.__repr__()}'
		s += f'\n	* pc_hitcheck_count = {self.pc_hitcheck_count.__repr__()}'
		s += f'\n	* pc_zero_0 = {self.pc_zero_0.__repr__()}'
		s += f'\n	* pc_floats = {self.pc_floats.__repr__()}'
		s += f'\n	* joint_indices = {self.joint_indices.__repr__()}'
		s += f'\n	* bone_indices = {self.bone_indices.__repr__()}'
		s += f'\n	* joint_names = {self.joint_names.__repr__()}'
		s += f'\n	* joint_names_padding = {self.joint_names_padding.__repr__()}'
		s += f'\n	* joint_info_list = {self.joint_info_list.__repr__()}'
		s += f'\n	* hitchecks_pc = {self.hitchecks_pc.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
