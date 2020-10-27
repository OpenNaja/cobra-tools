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
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# 4
		self.joint_count = 0

		# 0
		self.unknown_1 = 0

		# 0
		self.unknown_2 = 0

		# 0
		self.unknown_3 = 0
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
		self.joint_count = stream.read_uint()
		self.unknown_1 = stream.read_uint()
		self.unknown_2 = stream.read_uint()
		self.unknown_3 = stream.read_uint()
		self.joint_compound = stream.read_type(JointCompound)
		self.joint_list.read(stream, JointEntry, self.joint_count, None)
		self.unknown_list.read(stream, UnknownJointEntry, self.joint_count, None)
		self.unknown_10.read(stream, FFCounter, self.joint_count, None)
		self.unknown_11 = stream.read_uint()
		self.joint_names = stream.read_type(ZStringBuffer, (self.joint_compound.namespace_length,))
		self.joint_names_padding.read(stream, 'Byte', (4 - (self.joint_compound.namespace_length % 8)) % 8, None)
		self.joint_info_list.read(stream, JointInfo, self.joint_count, None)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.joint_count)
		stream.write_uint(self.unknown_1)
		stream.write_uint(self.unknown_2)
		stream.write_uint(self.unknown_3)
		stream.write_type(self.joint_compound)
		self.joint_list.write(stream, JointEntry, self.joint_count, None)
		self.unknown_list.write(stream, UnknownJointEntry, self.joint_count, None)
		self.unknown_10.write(stream, FFCounter, self.joint_count, None)
		stream.write_uint(self.unknown_11)
		stream.write_type(self.joint_names)
		self.joint_names_padding.write(stream, 'Byte', (4 - (self.joint_compound.namespace_length % 8)) % 8, None)
		self.joint_info_list.write(stream, JointInfo, self.joint_count, None)

		self.io_size = stream.tell() - self.io_start

	def __repr__(self):
		s = 'JointData [Size: '+str(self.io_size)+', Address:'+str(self.io_start)+']'
		s += '\n	* joint_count = ' + self.joint_count.__repr__()
		s += '\n	* unknown_1 = ' + self.unknown_1.__repr__()
		s += '\n	* unknown_2 = ' + self.unknown_2.__repr__()
		s += '\n	* unknown_3 = ' + self.unknown_3.__repr__()
		s += '\n	* joint_compound = ' + self.joint_compound.__repr__()
		s += '\n	* joint_list = ' + self.joint_list.__repr__()
		s += '\n	* unknown_list = ' + self.unknown_list.__repr__()
		s += '\n	* unknown_10 = ' + self.unknown_10.__repr__()
		s += '\n	* unknown_11 = ' + self.unknown_11.__repr__()
		s += '\n	* joint_names = ' + self.joint_names.__repr__()
		s += '\n	* joint_names_padding = ' + self.joint_names_padding.__repr__()
		s += '\n	* joint_info_list = ' + self.joint_info_list.__repr__()
		s += '\n'
		return s
