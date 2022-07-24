from source.formats.base.basic import fmt_member
import generated.formats.base.basic
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint64
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class IslandRoot(MemStruct):

	"""
	JWE2: 32 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.a = 0
		self.b = 0
		self.count = 0
		self.zero = 0
		self.path_name = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.a = 0.0
		self.b = 0.0
		self.count = 0
		self.zero = 0
		self.path_name = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.path_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.a = stream.read_float()
		instance.b = stream.read_float()
		instance.count = stream.read_uint64()
		instance.zero = stream.read_uint64()
		instance.path_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.path_name)
		stream.write_float(instance.a)
		stream.write_float(instance.b)
		stream.write_uint64(instance.count)
		stream.write_uint64(instance.zero)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('path_name', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('a', Float, (0, None))
		yield ('b', Float, (0, None))
		yield ('count', Uint64, (0, None))
		yield ('zero', Uint64, (0, None))

	def get_info_str(self, indent=0):
		return f'IslandRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* path_name = {fmt_member(self.path_name, indent+1)}'
		s += f'\n	* a = {fmt_member(self.a, indent+1)}'
		s += f'\n	* b = {fmt_member(self.b, indent+1)}'
		s += f'\n	* count = {fmt_member(self.count, indent+1)}'
		s += f'\n	* zero = {fmt_member(self.zero, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
