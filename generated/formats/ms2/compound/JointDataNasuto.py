import typing
from generated.array import Array
from generated.formats.ms2.compound.JointCompound import JointCompound
from generated.formats.ms2.compound.JointEntry import JointEntry
from generated.formats.ms2.compound.JointInfo import JointInfo
from generated.formats.ms2.compound.ListCEntry import ListCEntry
from generated.formats.ms2.compound.ListLong import ListLong
from generated.formats.ms2.compound.ListShort import ListShort
from generated.formats.ms2.compound.NasutoJointEntry import NasutoJointEntry
from generated.formats.ms2.compound.ZStringBuffer import ZStringBuffer


class JointDataNasuto:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# repeat
		self.count_7 = 0

		# 0
		self.unknown_2 = 0

		# 60 bytes per entry
		self.unknown_list = Array()

		# align list to multiples of 8
		self.padding = Array()

		# repeat
		self.joint_count = 0

		# small number
		self.count_0 = 0

		# small number
		self.count_1 = 0
		self.joint_compound = JointCompound()
		self.unknown_lista = Array()

		# might be pointers
		self.zeros = Array()
		self.unknown_listc = Array()

		# 3
		self.d = 0

		# 2
		self.e = 0
		self.short_list = Array()
		self.long_list = Array()

		# index
		self.indices = Array()

		# index or -1
		self.indices_2 = Array()
		self.joint_names = ZStringBuffer()
		self.joint_names_padding = Array()

		# 2
		self.zero_22 = 0
		self.joint_info_list = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.count_7 = stream.read_uint64()
		self.unknown_2 = stream.read_uint64()
		self.unknown_list.read(stream, NasutoJointEntry, self.count_7, None)
		self.padding = stream.read_ubytes(((8 - ((self.count_7 * 60) % 8)) % 8))
		self.joint_count = stream.read_uint64()
		self.count_0 = stream.read_uint()
		self.count_1 = stream.read_uint()
		self.joint_compound = stream.read_type(JointCompound)
		self.unknown_lista.read(stream, JointEntry, self.joint_count, None)
		self.zeros = stream.read_uint64s((self.joint_count))
		self.unknown_listc.read(stream, ListCEntry, self.joint_count, None)
		self.d = stream.read_ushort()
		self.e = stream.read_ushort()
		self.short_list.read(stream, ListShort, self.count_0, None)
		self.long_list.read(stream, ListLong, self.count_1, None)
		self.indices = stream.read_uints((self.joint_compound.joint_entry_count))
		self.indices_2 = stream.read_ints((self.joint_compound.bone_count))
		self.joint_names = stream.read_type(ZStringBuffer, (self.joint_compound.namespace_length,))
		self.joint_names_padding = stream.read_bytes(((8 - (self.joint_compound.namespace_length % 8)) % 8))
		self.zero_22 = stream.read_uint()
		self.joint_info_list.read(stream, JointInfo, 1, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64(self.count_7)
		stream.write_uint64(self.unknown_2)
		self.unknown_list.write(stream, NasutoJointEntry, self.count_7, None)
		stream.write_ubytes(self.padding)
		stream.write_uint64(self.joint_count)
		stream.write_uint(self.count_0)
		stream.write_uint(self.count_1)
		stream.write_type(self.joint_compound)
		self.unknown_lista.write(stream, JointEntry, self.joint_count, None)
		stream.write_uint64s(self.zeros)
		self.unknown_listc.write(stream, ListCEntry, self.joint_count, None)
		stream.write_ushort(self.d)
		stream.write_ushort(self.e)
		self.short_list.write(stream, ListShort, self.count_0, None)
		self.long_list.write(stream, ListLong, self.count_1, None)
		stream.write_uints(self.indices)
		stream.write_ints(self.indices_2)
		stream.write_type(self.joint_names)
		stream.write_bytes(self.joint_names_padding)
		stream.write_uint(self.zero_22)
		self.joint_info_list.write(stream, JointInfo, 1, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'JointDataNasuto [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* count_7 = {self.count_7.__repr__()}'
		s += f'\n	* unknown_2 = {self.unknown_2.__repr__()}'
		s += f'\n	* unknown_list = {self.unknown_list.__repr__()}'
		s += f'\n	* padding = {self.padding.__repr__()}'
		s += f'\n	* joint_count = {self.joint_count.__repr__()}'
		s += f'\n	* count_0 = {self.count_0.__repr__()}'
		s += f'\n	* count_1 = {self.count_1.__repr__()}'
		s += f'\n	* joint_compound = {self.joint_compound.__repr__()}'
		s += f'\n	* unknown_lista = {self.unknown_lista.__repr__()}'
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* unknown_listc = {self.unknown_listc.__repr__()}'
		s += f'\n	* d = {self.d.__repr__()}'
		s += f'\n	* e = {self.e.__repr__()}'
		s += f'\n	* short_list = {self.short_list.__repr__()}'
		s += f'\n	* long_list = {self.long_list.__repr__()}'
		s += f'\n	* indices = {self.indices.__repr__()}'
		s += f'\n	* indices_2 = {self.indices_2.__repr__()}'
		s += f'\n	* joint_names = {self.joint_names.__repr__()}'
		s += f'\n	* joint_names_padding = {self.joint_names_padding.__repr__()}'
		s += f'\n	* zero_22 = {self.zero_22.__repr__()}'
		s += f'\n	* joint_info_list = {self.joint_info_list.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
