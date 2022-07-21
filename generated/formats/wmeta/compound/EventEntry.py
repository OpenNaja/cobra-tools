from source.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class EventEntry(MemStruct):

	"""
	PC: 56 bytes
	JWE2: 40 bytes
	# todo - improve versioning
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default=False)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.hash = 0
		self.zero = 0
		self.zero_2 = 0
		self.size = 0
		self.flag_0 = 0
		self.flag_1 = 0
		self.flag_2 = 0
		self.zero_3 = 0
		self.flag_3 = 0
		self.hash_b = 0
		self.hash_c = 0
		self.zero_4 = 0
		self.u_2 = 0
		self.u_1 = 0
		self.block_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.hash = 0
		self.zero = 0
		if self.context.version <= 18:
			self.zero_2 = 0
		if self.context.version <= 18:
			self.size = 0
		self.flag_0 = 0
		self.flag_1 = 0
		self.flag_2 = 0
		if self.context.version <= 18:
			self.zero_3 = 0
		if self.context.version <= 18:
			self.flag_3 = 0
		self.hash_b = 0
		self.hash_c = 0
		self.zero_4 = 0
		if self.context.version >= 19:
			self.u_2 = 0
		if self.context.version >= 19:
			self.u_1 = 0
		if self.context.version <= 18:
			self.block_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.hash = stream.read_uint()
		instance.zero = stream.read_uint()
		if instance.context.version <= 18:
			instance.block_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
			instance.zero_2 = stream.read_ushort()
		if instance.context.version <= 18:
			instance.size = stream.read_ushort()
		instance.flag_0 = stream.read_uint()
		instance.flag_1 = stream.read_uint()
		instance.flag_2 = stream.read_uint()
		if instance.context.version <= 18:
			instance.zero_3 = stream.read_uint64()
			instance.flag_3 = stream.read_uint()
		instance.hash_b = stream.read_uint()
		instance.hash_c = stream.read_uint()
		instance.zero_4 = stream.read_uint()
		if instance.context.version >= 19:
			instance.u_2 = stream.read_uint()
			instance.u_1 = stream.read_uint()
		instance.block_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.hash)
		stream.write_uint(instance.zero)
		if instance.context.version <= 18:
			Pointer.to_stream(stream, instance.block_name)
			stream.write_ushort(instance.zero_2)
		if instance.context.version <= 18:
			stream.write_ushort(instance.size)
		stream.write_uint(instance.flag_0)
		stream.write_uint(instance.flag_1)
		stream.write_uint(instance.flag_2)
		if instance.context.version <= 18:
			stream.write_uint64(instance.zero_3)
			stream.write_uint(instance.flag_3)
		stream.write_uint(instance.hash_b)
		stream.write_uint(instance.hash_c)
		stream.write_uint(instance.zero_4)
		if instance.context.version >= 19:
			stream.write_uint(instance.u_2)
			stream.write_uint(instance.u_1)

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
		return f'EventEntry [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* hash = {fmt_member(self.hash, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		s += f'\n	* block_name = {fmt_member(self.block_name, indent+1)}'
		s += f'\n	* zero_2 = {fmt_member(self.zero_2, indent+1)}'
		s += f'\n	* size = {fmt_member(self.size, indent+1)}'
		s += f'\n	* flag_0 = {fmt_member(self.flag_0, indent+1)}'
		s += f'\n	* flag_1 = {fmt_member(self.flag_1, indent+1)}'
		s += f'\n	* flag_2 = {fmt_member(self.flag_2, indent+1)}'
		s += f'\n	* zero_3 = {fmt_member(self.zero_3, indent+1)}'
		s += f'\n	* flag_3 = {fmt_member(self.flag_3, indent+1)}'
		s += f'\n	* hash_b = {fmt_member(self.hash_b, indent+1)}'
		s += f'\n	* hash_c = {fmt_member(self.hash_c, indent+1)}'
		s += f'\n	* zero_4 = {fmt_member(self.zero_4, indent+1)}'
		s += f'\n	* u_2 = {fmt_member(self.u_2, indent+1)}'
		s += f'\n	* u_1 = {fmt_member(self.u_1, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
