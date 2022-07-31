from source.formats.base.basic import fmt_member
import generated.formats.base.basic
import numpy
from generated.formats.habitatboundary.compound.Vector3 import Vector3
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
		self.zeros = numpy.zeros((7,), dtype=numpy.dtype('uint64'))
		self.u_1 = 0
		self.u_2 = 0.0
		self.u_3 = 0
		self.opt_straight_curve = False
		self.opt_windows = False
		self.unk_vec_1 = Vector3(self.context, 0, None)
		self.unk_vec_2 = Vector3(self.context, 0, None)
		self.unk_vec_3 = Vector3(self.context, 0, None)
		self.unk_float_1 = 0.0

		# Posts of N Level can only use Walls of less than N Level
		self.wall_replace_level = 0

		# 0 = Glass, 1 = Null, 3 = Solid Opaques (Brick, Concrete), 4 = 1-Way Glass, 5 = Wire Fences, 7 = Electrified Wire Fence
		self.type = 0
		self.padding = 0
		self.prefab = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_end = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_top = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_bottom = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_post = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_extrusion = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_extrusion_pile = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_ground = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_1_m = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_10_m = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.post = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.post_cap = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.u_0 = 0
		self.zeros = numpy.zeros((7,), dtype=numpy.dtype('uint64'))
		self.u_1 = 0
		self.u_2 = 0.0
		self.u_3 = 0
		self.opt_straight_curve = False
		self.opt_windows = False
		self.unk_vec_1 = Vector3(self.context, 0, None)
		self.unk_vec_2 = Vector3(self.context, 0, None)
		self.unk_vec_3 = Vector3(self.context, 0, None)
		self.unk_float_1 = 0.0
		self.wall_replace_level = 0
		self.type = 0
		self.padding = 0
		self.prefab = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_end = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_top = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.walls_extrusion_bottom = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_post = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_extrusion = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_extrusion_pile = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_ground = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_1_m = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.broken_10_m = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.post = Pointer(self.context, 0, generated.formats.base.basic.ZString)
		self.post_cap = Pointer(self.context, 0, generated.formats.base.basic.ZString)

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
		instance.prefab = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion_end = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.walls_extrusion_top = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.u_0 = stream.read_uint64()
		instance.walls_extrusion_bottom = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.zeros = stream.read_uint64s((7,))
		instance.broken_post = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.broken_extrusion = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.broken_extrusion_pile = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.broken_ground = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.broken_1_m = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.broken_10_m = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.post = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.post_cap = Pointer.from_stream(stream, instance.context, 0, generated.formats.base.basic.ZString)
		instance.u_1 = stream.read_uint()
		instance.u_2 = stream.read_float()
		instance.u_3 = stream.read_ushort()
		instance.opt_straight_curve = stream.read_bool()
		instance.opt_windows = stream.read_bool()
		instance.unk_vec_1 = Vector3.from_stream(stream, instance.context, 0, None)
		instance.unk_vec_2 = Vector3.from_stream(stream, instance.context, 0, None)
		instance.unk_vec_3 = Vector3.from_stream(stream, instance.context, 0, None)
		instance.unk_float_1 = stream.read_float()
		instance.wall_replace_level = stream.read_byte()
		instance.type = stream.read_byte()
		instance.padding = stream.read_ushort()
		instance.prefab.arg = 0
		instance.walls_extrusion.arg = 0
		instance.walls_extrusion_end.arg = 0
		instance.walls_extrusion_top.arg = 0
		instance.walls_extrusion_bottom.arg = 0
		instance.broken_post.arg = 0
		instance.broken_extrusion.arg = 0
		instance.broken_extrusion_pile.arg = 0
		instance.broken_ground.arg = 0
		instance.broken_1_m.arg = 0
		instance.broken_10_m.arg = 0
		instance.post.arg = 0
		instance.post_cap.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.prefab)
		Pointer.to_stream(stream, instance.walls_extrusion)
		Pointer.to_stream(stream, instance.walls_extrusion_end)
		Pointer.to_stream(stream, instance.walls_extrusion_top)
		stream.write_uint64(instance.u_0)
		Pointer.to_stream(stream, instance.walls_extrusion_bottom)
		stream.write_uint64s(instance.zeros)
		Pointer.to_stream(stream, instance.broken_post)
		Pointer.to_stream(stream, instance.broken_extrusion)
		Pointer.to_stream(stream, instance.broken_extrusion_pile)
		Pointer.to_stream(stream, instance.broken_ground)
		Pointer.to_stream(stream, instance.broken_1_m)
		Pointer.to_stream(stream, instance.broken_10_m)
		Pointer.to_stream(stream, instance.post)
		Pointer.to_stream(stream, instance.post_cap)
		stream.write_uint(instance.u_1)
		stream.write_float(instance.u_2)
		stream.write_ushort(instance.u_3)
		stream.write_bool(instance.opt_straight_curve)
		stream.write_bool(instance.opt_windows)
		Vector3.to_stream(stream, instance.unk_vec_1)
		Vector3.to_stream(stream, instance.unk_vec_2)
		Vector3.to_stream(stream, instance.unk_vec_3)
		stream.write_float(instance.unk_float_1)
		stream.write_byte(instance.wall_replace_level)
		stream.write_byte(instance.type)
		stream.write_ushort(instance.padding)

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
		return f'HabitatBoundaryDataRoot [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* prefab = {fmt_member(self.prefab, indent+1)}'
		s += f'\n	* walls_extrusion = {fmt_member(self.walls_extrusion, indent+1)}'
		s += f'\n	* walls_extrusion_end = {fmt_member(self.walls_extrusion_end, indent+1)}'
		s += f'\n	* walls_extrusion_top = {fmt_member(self.walls_extrusion_top, indent+1)}'
		s += f'\n	* u_0 = {fmt_member(self.u_0, indent+1)}'
		s += f'\n	* walls_extrusion_bottom = {fmt_member(self.walls_extrusion_bottom, indent+1)}'
		s += f'\n	* zeros = {fmt_member(self.zeros, indent+1)}'
		s += f'\n	* broken_post = {fmt_member(self.broken_post, indent+1)}'
		s += f'\n	* broken_extrusion = {fmt_member(self.broken_extrusion, indent+1)}'
		s += f'\n	* broken_extrusion_pile = {fmt_member(self.broken_extrusion_pile, indent+1)}'
		s += f'\n	* broken_ground = {fmt_member(self.broken_ground, indent+1)}'
		s += f'\n	* broken_1_m = {fmt_member(self.broken_1_m, indent+1)}'
		s += f'\n	* broken_10_m = {fmt_member(self.broken_10_m, indent+1)}'
		s += f'\n	* post = {fmt_member(self.post, indent+1)}'
		s += f'\n	* post_cap = {fmt_member(self.post_cap, indent+1)}'
		s += f'\n	* u_1 = {fmt_member(self.u_1, indent+1)}'
		s += f'\n	* u_2 = {fmt_member(self.u_2, indent+1)}'
		s += f'\n	* u_3 = {fmt_member(self.u_3, indent+1)}'
		s += f'\n	* opt_straight_curve = {fmt_member(self.opt_straight_curve, indent+1)}'
		s += f'\n	* opt_windows = {fmt_member(self.opt_windows, indent+1)}'
		s += f'\n	* unk_vec_1 = {fmt_member(self.unk_vec_1, indent+1)}'
		s += f'\n	* unk_vec_2 = {fmt_member(self.unk_vec_2, indent+1)}'
		s += f'\n	* unk_vec_3 = {fmt_member(self.unk_vec_3, indent+1)}'
		s += f'\n	* unk_float_1 = {fmt_member(self.unk_float_1, indent+1)}'
		s += f'\n	* wall_replace_level = {fmt_member(self.wall_replace_level, indent+1)}'
		s += f'\n	* type = {fmt_member(self.type, indent+1)}'
		s += f'\n	* padding = {fmt_member(self.padding, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
