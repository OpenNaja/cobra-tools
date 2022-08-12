from generated.formats.base.basic import fmt_member
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Int
from generated.formats.base.basic import Short
from generated.formats.base.basic import Uint64
from generated.formats.fct.compound.Font import Font
from generated.formats.ovl_base.compound.MemStruct import MemStruct


class FctRoot(MemStruct):

	"""
	JWE1: 104 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.u_0 = 0
		self.u_1 = 0
		self.a = 0
		self.b = 0
		self.c = 0
		self.minus_1 = 0
		self.z_0 = 0
		self.z_1 = 0
		self.z_2 = 0
		self.offset = 0
		self.fonts = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		print(f'set_defaults {self.__class__.__name__}')
		self.u_0 = 0
		self.u_1 = 0
		self.a = 0.0
		self.b = 0.0
		self.c = 0.0
		self.minus_1 = 0
		self.z_0 = 0
		self.z_1 = 0
		self.z_2 = 0
		self.offset = 0
		self.fonts = Array((4,), Font, self.context, 0, None)

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
		instance.u_0 = stream.read_short()
		instance.u_1 = stream.read_short()
		instance.a = stream.read_float()
		instance.b = stream.read_float()
		instance.c = stream.read_float()
		instance.minus_1 = stream.read_short()
		instance.z_0 = stream.read_short()
		instance.z_1 = stream.read_int()
		instance.z_2 = stream.read_uint64()
		instance.offset = stream.read_uint64()
		instance.fonts = Array.from_stream(stream, (4,), Font, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		stream.write_short(instance.u_0)
		stream.write_short(instance.u_1)
		stream.write_float(instance.a)
		stream.write_float(instance.b)
		stream.write_float(instance.c)
		stream.write_short(instance.minus_1)
		stream.write_short(instance.z_0)
		stream.write_int(instance.z_1)
		stream.write_uint64(instance.z_2)
		stream.write_uint64(instance.offset)
		Array.to_stream(stream, instance.fonts, (4,), Font, instance.context, 0, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('u_0', Short, (0, None))
		yield ('u_1', Short, (0, None))
		yield ('a', Float, (0, None))
		yield ('b', Float, (0, None))
		yield ('c', Float, (0, None))
		yield ('minus_1', Short, (0, None))
		yield ('z_0', Short, (0, None))
		yield ('z_1', Int, (0, None))
		yield ('z_2', Uint64, (0, None))
		yield ('offset', Uint64, (0, None))
		yield ('fonts', Array, ((4,), Font, 0, None))

	def get_info_str(self, indent=0):
		return f'FctRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* u_0 = {fmt_member(self.u_0, indent+1)}'
		s += f'\n	* u_1 = {fmt_member(self.u_1, indent+1)}'
		s += f'\n	* a = {fmt_member(self.a, indent+1)}'
		s += f'\n	* b = {fmt_member(self.b, indent+1)}'
		s += f'\n	* c = {fmt_member(self.c, indent+1)}'
		s += f'\n	* minus_1 = {fmt_member(self.minus_1, indent+1)}'
		s += f'\n	* z_0 = {fmt_member(self.z_0, indent+1)}'
		s += f'\n	* z_1 = {fmt_member(self.z_1, indent+1)}'
		s += f'\n	* z_2 = {fmt_member(self.z_2, indent+1)}'
		s += f'\n	* offset = {fmt_member(self.offset, indent+1)}'
		s += f'\n	* fonts = {fmt_member(self.fonts, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
