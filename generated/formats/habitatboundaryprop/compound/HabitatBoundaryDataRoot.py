from generated.formats.base.basic import fmt_member
import generated.formats.base.basic
import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import Ushort
from generated.formats.ovl_base.compound.MemStruct import MemStruct
from generated.formats.ovl_base.compound.Pointer import Pointer


class HabitatBoundaryDataRoot(MemStruct):

	"""
	224 bytes
	"""

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		super().__init__(context, arg, template, set_default)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.u_0 = 0
		self.zeros = 0
		self.u_1 = 0
		self.u_2 = 0
		self.u_3 = 0
		self.u_4 = 0
		self.floats = 0
		self.u_5 = 0
		self.name_a = 0
		self.walls_extrusion = 0
		self.walls_extrusion_end = 0
		self.walls_extrusion_top = 0
		self.walls_extrusion_bottom = 0
		self.name_f = 0
		self.name_g = 0
		self.name_h = 0
		self.name_i = 0
		self.name_j = 0
		self.name_k = 0
		self.name_l = 0
		self.name_m = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.u_0 = 0
		self.zeros = numpy.zeros((7,), dtype=numpy.dtype('uint64'))
		self.u_1 = 0
		self.u_2 = 0.0
		self.u_3 = 0
		self.u_4 = 0
		self.floats = numpy.zeros((10,), dtype=numpy.dtype('float32'))
		self.u_5 = 0
		self.name_a = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_end = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_top = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_bottom = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.name_f = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.name_g = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.name_h = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.name_i = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.name_j = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.name_k = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.name_l = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.name_m = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.name_a = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion_end = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion_top = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.u_0 = stream.read_uint64()
		instance.walls_extrusion_bottom = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.zeros = stream.read_uint64s((7,))
		instance.name_f = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.name_g = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.name_h = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.name_i = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.name_j = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.name_k = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.name_l = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.name_m = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.u_1 = stream.read_uint()
		instance.u_2 = stream.read_float()
		instance.u_3 = stream.read_ushort()
		instance.u_4 = stream.read_ushort()
		instance.floats = stream.read_floats((10,))
		instance.u_5 = stream.read_uint()
		instance.name_a.arg = 0
		instance.walls_extrusion.arg = 0
		instance.walls_extrusion_end.arg = 0
		instance.walls_extrusion_top.arg = 0
		instance.walls_extrusion_bottom.arg = 0
		instance.name_f.arg = 0
		instance.name_g.arg = 0
		instance.name_h.arg = 0
		instance.name_i.arg = 0
		instance.name_j.arg = 0
		instance.name_k.arg = 0
		instance.name_l.arg = 0
		instance.name_m.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.name_a)
		Pointer.to_stream(stream, instance.walls_extrusion)
		Pointer.to_stream(stream, instance.walls_extrusion_end)
		Pointer.to_stream(stream, instance.walls_extrusion_top)
		stream.write_uint64(instance.u_0)
		Pointer.to_stream(stream, instance.walls_extrusion_bottom)
		stream.write_uint64s(instance.zeros)
		Pointer.to_stream(stream, instance.name_f)
		Pointer.to_stream(stream, instance.name_g)
		Pointer.to_stream(stream, instance.name_h)
		Pointer.to_stream(stream, instance.name_i)
		Pointer.to_stream(stream, instance.name_j)
		Pointer.to_stream(stream, instance.name_k)
		Pointer.to_stream(stream, instance.name_l)
		Pointer.to_stream(stream, instance.name_m)
		stream.write_uint(instance.u_1)
		stream.write_float(instance.u_2)
		stream.write_ushort(instance.u_3)
		stream.write_ushort(instance.u_4)
		stream.write_floats(instance.floats)
		stream.write_uint(instance.u_5)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		super()._get_filtered_attribute_list(instance)
		yield ('name_a', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('walls_extrusion', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('walls_extrusion_end', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('walls_extrusion_top', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('u_0', Uint64, (0, None))
		yield ('walls_extrusion_bottom', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('zeros', Array, ((7,), Uint64, 0, None))
		yield ('name_f', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('name_g', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('name_h', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('name_i', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('name_j', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('name_k', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('name_l', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('name_m', Pointer, (0, generated.formats.base.basic.ZString))
		yield ('u_1', Uint, (0, None))
		yield ('u_2', Float, (0, None))
		yield ('u_3', Ushort, (0, None))
		yield ('u_4', Ushort, (0, None))
		yield ('floats', Array, ((10,), Float, 0, None))
		yield ('u_5', Uint, (0, None))

	def get_info_str(self, indent=0):
		return f'HabitatBoundaryDataRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* name_a = {fmt_member(self.name_a, indent+1)}'
		s += f'\n	* walls_extrusion = {fmt_member(self.walls_extrusion, indent+1)}'
		s += f'\n	* walls_extrusion_end = {fmt_member(self.walls_extrusion_end, indent+1)}'
		s += f'\n	* walls_extrusion_top = {fmt_member(self.walls_extrusion_top, indent+1)}'
		s += f'\n	* u_0 = {fmt_member(self.u_0, indent+1)}'
		s += f'\n	* walls_extrusion_bottom = {fmt_member(self.walls_extrusion_bottom, indent+1)}'
		s += f'\n	* zeros = {fmt_member(self.zeros, indent+1)}'
		s += f'\n	* name_f = {fmt_member(self.name_f, indent+1)}'
		s += f'\n	* name_g = {fmt_member(self.name_g, indent+1)}'
		s += f'\n	* name_h = {fmt_member(self.name_h, indent+1)}'
		s += f'\n	* name_i = {fmt_member(self.name_i, indent+1)}'
		s += f'\n	* name_j = {fmt_member(self.name_j, indent+1)}'
		s += f'\n	* name_k = {fmt_member(self.name_k, indent+1)}'
		s += f'\n	* name_l = {fmt_member(self.name_l, indent+1)}'
		s += f'\n	* name_m = {fmt_member(self.name_m, indent+1)}'
		s += f'\n	* u_1 = {fmt_member(self.u_1, indent+1)}'
		s += f'\n	* u_2 = {fmt_member(self.u_2, indent+1)}'
		s += f'\n	* u_3 = {fmt_member(self.u_3, indent+1)}'
		s += f'\n	* u_4 = {fmt_member(self.u_4, indent+1)}'
		s += f'\n	* floats = {fmt_member(self.floats, indent+1)}'
		s += f'\n	* u_5 = {fmt_member(self.u_5, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
