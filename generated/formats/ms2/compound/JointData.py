import typing
from generated.formats.ms2.compound.FFCounter import FFCounter
from generated.formats.ms2.compound.JointCompound import JointCompound
from generated.formats.ms2.compound.JointEntry import JointEntry
from generated.formats.ms2.compound.JointInfo import JointInfo
from generated.formats.ms2.compound.UnknownJointEntry import UnknownJointEntry
from generated.formats.ms2.compound.ZStringBuffer import ZStringBuffer


class JointData:

	# 4
	joint_count: int

	# 0
	unknown_1: int

	# 0
	unknown_2: int

	# 0
	unknown_3: int
	joint_compound: JointCompound
	joint_list: typing.List[JointEntry]
	unknown_list: typing.List[UnknownJointEntry]
	unknown_10: typing.List[FFCounter]
	unknown_11: int
	joint_names: ZStringBuffer
	joint_names_padding: typing.List[int]
	joint_info_list: typing.List[JointInfo]

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.joint_count = 0
		self.unknown_1 = 0
		self.unknown_2 = 0
		self.unknown_3 = 0
		self.joint_compound = JointCompound()
		self.joint_list = []
		self.unknown_list = []
		self.unknown_10 = []
		self.unknown_11 = 0
		self.joint_names = ZStringBuffer()
		self.joint_names_padding = []
		self.joint_info_list = []

	def read(self, stream):

		self.io_start = stream.tell()
		self.joint_count = stream.read_uint()
		self.unknown_1 = stream.read_uint()
		self.unknown_2 = stream.read_uint()
		self.unknown_3 = stream.read_uint()
		self.joint_compound = stream.read_type(JointCompound)
		self.joint_list = [stream.read_type(JointEntry) for _ in range(self.joint_count)]
		self.unknown_list = [stream.read_type(UnknownJointEntry) for _ in range(self.joint_count)]
		self.unknown_10 = [stream.read_type(FFCounter) for _ in range(self.joint_count)]
		self.unknown_11 = stream.read_uint()
		self.joint_names = stream.read_type(ZStringBuffer, (self.joint_compound.namespace_length,))
		self.joint_names_padding = [stream.read_byte() for _ in range((4 - (self.joint_compound.namespace_length % 8)) % 8)]
		self.joint_info_list = [stream.read_type(JointInfo) for _ in range(self.joint_count)]

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.joint_count)
		stream.write_uint(self.unknown_1)
		stream.write_uint(self.unknown_2)
		stream.write_uint(self.unknown_3)
		stream.write_type(self.joint_compound)
		for item in self.joint_list: stream.write_type(item)
		for item in self.unknown_list: stream.write_type(item)
		for item in self.unknown_10: stream.write_type(item)
		stream.write_uint(self.unknown_11)
		stream.write_type(self.joint_names)
		for item in self.joint_names_padding: stream.write_byte(item)
		for item in self.joint_info_list: stream.write_type(item)

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
