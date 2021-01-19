import typing
from generated.array import Array
from generated.formats.ms2.compound.FFCounter import FFCounter
from generated.formats.ms2.compound.JointCompound import JointCompound
from generated.formats.ms2.compound.JointEntry import JointEntry
from generated.formats.ms2.compound.JointInfo import JointInfo
from generated.formats.ms2.compound.UnknownJointEntry import UnknownJointEntry
from generated.formats.ms2.compound.ZStringBuffer import ZStringBuffer


class JointData:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.joint_compound = JointCompound()
		self.joint_list = Array()
		self.unknown_list = Array()
		self.unknown_10 = Array()
		self.unknown_11 = 0
		self.joint_names = ZStringBuffer()
		self.joint_names_padding = Array()
		self.joint_info_list = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.joint_compound = stream.read_type(JointCompound)
		self.joint_list.read(stream, JointEntry, self.joint_compound.joint_count, None)
		self.unknown_list.read(stream, UnknownJointEntry, self.joint_compound.joint_count, None)
		self.unknown_10.read(stream, FFCounter, self.joint_compound.joint_count, None)
		self.unknown_11 = stream.read_uint()
		self.joint_names = stream.read_type(ZStringBuffer, (self.joint_compound.namespace_length,))
		self.joint_names_padding = stream.read_bytes(((4 - (self.joint_compound.namespace_length % 8)) % 8))
		self.joint_info_list.read(stream, JointInfo, self.joint_compound.joint_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_type(self.joint_compound)
		self.joint_list.write(stream, JointEntry, self.joint_compound.joint_count, None)
		self.unknown_list.write(stream, UnknownJointEntry, self.joint_compound.joint_count, None)
		self.unknown_10.write(stream, FFCounter, self.joint_compound.joint_count, None)
		stream.write_uint(self.unknown_11)
		stream.write_type(self.joint_names)
		stream.write_bytes(self.joint_names_padding)
		self.joint_info_list.write(stream, JointInfo, self.joint_compound.joint_count, None)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'JointData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* joint_compound = {self.joint_compound.__repr__()}'
		s += f'\n	* joint_list = {self.joint_list.__repr__()}'
		s += f'\n	* unknown_list = {self.unknown_list.__repr__()}'
		s += f'\n	* unknown_10 = {self.unknown_10.__repr__()}'
		s += f'\n	* unknown_11 = {self.unknown_11.__repr__()}'
		s += f'\n	* joint_names = {self.joint_names.__repr__()}'
		s += f'\n	* joint_names_padding = {self.joint_names_padding.__repr__()}'
		s += f'\n	* joint_info_list = {self.joint_info_list.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
