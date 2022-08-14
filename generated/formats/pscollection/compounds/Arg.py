from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class Arg(MemStruct):

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_0 = 0
		self.arg_type = 0

		# one-based index
		self.arg_index = 0
		self.u_1 = 0
		self.u_2 = 0
		self.u_3 = 0
		self.u_4 = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.u_0 = 0
		self.arg_type = 0
		self.arg_index = 0
		self.u_1 = 0
		self.u_2 = 0
		self.u_3 = 0
		self.u_4 = 0

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
		instance.u_0 = stream.read_ubyte()
		instance.arg_type = stream.read_ubyte()
		instance.arg_index = stream.read_ubyte()
		instance.u_1 = stream.read_ubyte()
		instance.u_2 = stream.read_uint()
		instance.u_3 = stream.read_uint64()
		instance.u_4 = stream.read_uint64()

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_ubyte(instance.u_0)
		stream.write_ubyte(instance.arg_type)
		stream.write_ubyte(instance.arg_index)
		stream.write_ubyte(instance.u_1)
		stream.write_uint(instance.u_2)
		stream.write_uint64(instance.u_3)
		stream.write_uint64(instance.u_4)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield 'u_0', Ubyte, (0, None)
		yield 'arg_type', Ubyte, (0, None)
		yield 'arg_index', Ubyte, (0, None)
		yield 'u_1', Ubyte, (0, None)
		yield 'u_2', Uint, (0, None)
		yield 'u_3', Uint64, (0, None)
		yield 'u_4', Uint64, (0, None)

	def get_info_str(self, indent=0):
		return f'Arg [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* u_0 = {self.fmt_member(self.u_0, indent+1)}'
		s += f'\n	* arg_type = {self.fmt_member(self.arg_type, indent+1)}'
		s += f'\n	* arg_index = {self.fmt_member(self.arg_index, indent+1)}'
		s += f'\n	* u_1 = {self.fmt_member(self.u_1, indent+1)}'
		s += f'\n	* u_2 = {self.fmt_member(self.u_2, indent+1)}'
		s += f'\n	* u_3 = {self.fmt_member(self.u_3, indent+1)}'
		s += f'\n	* u_4 = {self.fmt_member(self.u_4, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
