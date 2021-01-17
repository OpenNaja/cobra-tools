import typing
from generated.array import Array
from generated.formats.ms2.compound.JointCompound import JointCompound
from generated.formats.ms2.compound.JointEntry import JointEntry
from generated.formats.ms2.compound.ListCEntry import ListCEntry
from generated.formats.ms2.compound.ListDEntry import ListDEntry
from generated.formats.ms2.compound.NasutoJointEntry import NasutoJointEntry


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
		self.unknown_listd = Array()

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
		self.unknown_listd.read(stream, ListDEntry, self.arg, None)

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
		self.unknown_listd.write(stream, ListDEntry, self.arg, None)

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
		s += f'\n	* unknown_listd = {self.unknown_listd.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
