from source.formats.base.basic import fmt_member
import numpy
from generated.array import Array
from generated.context import ContextReference
from generated.formats.ms2.compound.NasutoJointEntry import NasutoJointEntry
from generated.formats.ms2.compound.UACJoint import UACJoint
from generated.formats.ovl_base.compound.SmartPadding import SmartPadding


class Struct7:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# needed for ZTUAC
		self.weird_padding = 0

		# repeat
		self.count_7 = 0

		# seen 0
		self.zero_0 = 0

		# seen 0, 2, 4
		self.flag = 0
		self.zero_2 = 0

		# 36 bytes per entry
		self.unknown_list = 0

		# 60 bytes per entry
		self.unknown_list = 0

		# align list to multiples of 8
		self.padding = 0

		# latest PZ and jwe2 only - if flag is non-zero, 8 bytes, else 0
		self.alignment = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		if self.context.version <= 13:
			self.weird_padding = SmartPadding(self.context, 0, None)
		self.count_7 = 0
		self.zero_0 = 0
		if self.context.version >= 48:
			self.flag = 0
		if self.context.version >= 48:
			self.zero_2 = 0
		if self.context.version <= 13:
			self.unknown_list = Array((self.count_7,), UACJoint, self.context, 0, None)
		if self.context.version >= 32:
			self.unknown_list = Array((self.count_7,), NasutoJointEntry, self.context, 0, None)
		self.padding = numpy.zeros(((8 - ((self.count_7 * 60) % 8)) % 8,), dtype=numpy.dtype('uint8'))
		if self.context.version >= 50 and self.flag:
			self.alignment = 0

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		if instance.context.version <= 13:
			instance.weird_padding = SmartPadding.from_stream(stream, instance.context, 0, None)
		instance.count_7 = stream.read_uint64()
		instance.zero_0 = stream.read_uint64()
		if instance.context.version >= 48:
			instance.flag = stream.read_uint64()
			instance.zero_2 = stream.read_uint64()
		if instance.context.version <= 13:
			instance.unknown_list = Array.from_stream(stream, (instance.count_7,), UACJoint, instance.context, 0, None)
		if instance.context.version >= 32:
			instance.unknown_list = Array.from_stream(stream, (instance.count_7,), NasutoJointEntry, instance.context, 0, None)
		instance.padding = stream.read_ubytes(((8 - ((instance.count_7 * 60) % 8)) % 8,))
		if instance.context.version >= 50 and instance.flag:
			instance.alignment = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		if instance.context.version <= 13:
			SmartPadding.to_stream(stream, instance.weird_padding)
		stream.write_uint64(instance.count_7)
		stream.write_uint64(instance.zero_0)
		if instance.context.version >= 48:
			stream.write_uint64(instance.flag)
			stream.write_uint64(instance.zero_2)
		if instance.context.version <= 13:
			Array.to_stream(stream, instance.unknown_list, (instance.count_7,), UACJoint, instance.context, 0, None)
		if instance.context.version >= 32:
			Array.to_stream(stream, instance.unknown_list, (instance.count_7,), NasutoJointEntry, instance.context, 0, None)
		stream.write_ubytes(instance.padding)
		if instance.context.version >= 50 and instance.flag:
			stream.write_uint64(instance.alignment)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self, indent=0):
		return f'Struct7 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += f'\n	* weird_padding = {fmt_member(self.weird_padding, indent+1)}'
		s += f'\n	* count_7 = {fmt_member(self.count_7, indent+1)}'
		s += f'\n	* zero_0 = {fmt_member(self.zero_0, indent+1)}'
		s += f'\n	* flag = {fmt_member(self.flag, indent+1)}'
		s += f'\n	* zero_2 = {fmt_member(self.zero_2, indent+1)}'
		s += f'\n	* unknown_list = {fmt_member(self.unknown_list, indent+1)}'
		s += f'\n	* padding = {fmt_member(self.padding, indent+1)}'
		s += f'\n	* alignment = {fmt_member(self.alignment, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
