from source.formats.base.basic import fmt_member
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class WmetasbChild(MemStruct):

	"""
	40 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.hash = 0
		self.float_limit = 0.0
		self.c_0 = 0
		self.c_1 = 0
		self.c_2 = 0
		self.hash_2 = 0
		self.hash_3 = 0
		self.u_0 = 0
		self.u_1 = 0
		self.u_2 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.hash = 0
		self.float_limit = 0.0
		self.c_0 = 0
		self.c_1 = 0
		self.c_2 = 0
		self.hash_2 = 0
		self.hash_3 = 0
		self.u_0 = 0
		self.u_1 = 0
		self.u_2 = 0

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
		instance.float_limit = stream.read_float()
		instance.c_0 = stream.read_uint()
		instance.c_1 = stream.read_uint()
		instance.c_2 = stream.read_uint()
		instance.hash_2 = stream.read_uint()
		instance.hash_3 = stream.read_uint()
		instance.u_0 = stream.read_uint()
		instance.u_1 = stream.read_uint()
		instance.u_2 = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_uint(instance.hash)
		stream.write_float(instance.float_limit)
		stream.write_uint(instance.c_0)
		stream.write_uint(instance.c_1)
		stream.write_uint(instance.c_2)
		stream.write_uint(instance.hash_2)
		stream.write_uint(instance.hash_3)
		stream.write_uint(instance.u_0)
		stream.write_uint(instance.u_1)
		stream.write_uint(instance.u_2)

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
		return f'WmetasbChild [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* hash = {fmt_member(self.hash, indent+1)}'
		s += f'\n	* float_limit = {fmt_member(self.float_limit, indent+1)}'
		s += f'\n	* c_0 = {fmt_member(self.c_0, indent+1)}'
		s += f'\n	* c_1 = {fmt_member(self.c_1, indent+1)}'
		s += f'\n	* c_2 = {fmt_member(self.c_2, indent+1)}'
		s += f'\n	* hash_2 = {fmt_member(self.hash_2, indent+1)}'
		s += f'\n	* hash_3 = {fmt_member(self.hash_3, indent+1)}'
		s += f'\n	* u_0 = {fmt_member(self.u_0, indent+1)}'
		s += f'\n	* u_1 = {fmt_member(self.u_1, indent+1)}'
		s += f'\n	* u_2 = {fmt_member(self.u_2, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
