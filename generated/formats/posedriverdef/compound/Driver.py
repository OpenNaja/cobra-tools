from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import generated.formats.posedriverdef.compound.Data
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class Driver(MemStruct):

	"""
	48 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default=False)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.unk_1 = 0
		self.unk_2 = 0
		self.joint_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.driven_joint_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.data = Pointer(self.context, 0, generated.formats.posedriverdef.compound.Data.Data)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.a = 0
		self.b = 0
		self.c = 0
		self.d = 0
		self.unk_1 = 0
		self.unk_2 = 0
		self.joint_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.driven_joint_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.data = Pointer(self.context, 0, generated.formats.posedriverdef.compound.Data.Data)

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
		super().read_fields(stream, instance)
		instance.joint_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.a = stream.read_ubyte()
		instance.b = stream.read_ubyte()
		instance.c = stream.read_ushort()
		instance.d = stream.read_uint()
		instance.driven_joint_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.unk_1 = stream.read_uint64()
		instance.data = Pointer.from_stream(stream, instance.context, 0, generated.formats.posedriverdef.compound.Data.Data)
		instance.unk_2 = stream.read_uint64()
		instance.joint_name.arg = 0
		instance.driven_joint_name.arg = 0
		instance.data.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.joint_name)
		stream.write_ubyte(instance.a)
		stream.write_ubyte(instance.b)
		stream.write_ushort(instance.c)
		stream.write_uint(instance.d)
		Pointer.to_stream(stream, instance.driven_joint_name)
		stream.write_uint64(instance.unk_1)
		Pointer.to_stream(stream, instance.data)
		stream.write_uint64(instance.unk_2)

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
		return f'Driver [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* joint_name = {fmt_member(self.joint_name, indent+1)}'
		s += f'\n	* a = {fmt_member(self.a, indent+1)}'
		s += f'\n	* b = {fmt_member(self.b, indent+1)}'
		s += f'\n	* c = {fmt_member(self.c, indent+1)}'
		s += f'\n	* d = {fmt_member(self.d, indent+1)}'
		s += f'\n	* driven_joint_name = {fmt_member(self.driven_joint_name, indent+1)}'
		s += f'\n	* unk_1 = {fmt_member(self.unk_1, indent+1)}'
		s += f'\n	* data = {fmt_member(self.data, indent+1)}'
		s += f'\n	* unk_2 = {fmt_member(self.unk_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
