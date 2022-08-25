import generated.formats.ovl_base.basic
import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.dinosaurmaterialvariants.compounds.Vector3F import Vector3F
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DinoEffectsHeader(MemStruct):

	__name__ = DinoEffectsHeader

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.vec_0 = Vector3F(self.context, 0, None)
		self.vec_1 = Vector3F(self.context, 0, None)
		self.a = 0
		self.b = 0
		self.vec_2 = Vector3F(self.context, 0, None)
		self.vec_3 = Vector3F(self.context, 0, None)
		self.vec_4 = Vector3F(self.context, 0, None)
		self.c = 0
		self.d = 0
		self.e = 0.0
		self.f = 0.0
		self.g = 0
		self.floats = Array((0,), Float, self.context, 0, None)
		self.d = 0
		self.e = 0.0
		self.fgm_name = Pointer(self.context, 0, generated.formats.ovl_base.basic.ZStringObfuscated)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		super().set_defaults()
		self.vec_0 = Vector3F(self.context, 0, None)
		self.vec_1 = Vector3F(self.context, 0, None)
		self.a = 0
		self.b = 0
		self.vec_2 = Vector3F(self.context, 0, None)
		self.vec_3 = Vector3F(self.context, 0, None)
		self.vec_4 = Vector3F(self.context, 0, None)
		self.c = 0
		self.d = 0
		self.e = 0.0
		self.f = 0.0
		self.g = 0
		self.floats = numpy.zeros((39,), dtype=numpy.dtype('float32'))
		self.d = 0
		self.e = 0.0
		self.fgm_name = Pointer(self.context, 0, generated.formats.ovl_base.basic.ZStringObfuscated)

	@classmethod
	def read_fields(cls, stream, instance):
		super().read_fields(stream, instance)
		instance.fgm_name = Pointer.from_stream(stream, instance.context, 0, generated.formats.ovl_base.basic.ZStringObfuscated)
		instance.vec_0 = Vector3F.from_stream(stream, instance.context, 0, None)
		instance.vec_1 = Vector3F.from_stream(stream, instance.context, 0, None)
		instance.a = Uint.from_stream(stream, instance.context, 0, None)
		instance.b = Uint.from_stream(stream, instance.context, 0, None)
		instance.vec_2 = Vector3F.from_stream(stream, instance.context, 0, None)
		instance.vec_3 = Vector3F.from_stream(stream, instance.context, 0, None)
		instance.vec_4 = Vector3F.from_stream(stream, instance.context, 0, None)
		instance.c = Uint.from_stream(stream, instance.context, 0, None)
		instance.d = Uint.from_stream(stream, instance.context, 0, None)
		instance.e = Float.from_stream(stream, instance.context, 0, None)
		instance.f = Float.from_stream(stream, instance.context, 0, None)
		instance.g = Uint.from_stream(stream, instance.context, 0, None)
		instance.floats = Array.from_stream(stream, instance.context, 0, None, (39,), Float)
		instance.d = Uint.from_stream(stream, instance.context, 0, None)
		instance.e = Float.from_stream(stream, instance.context, 0, None)
		if not isinstance(instance.fgm_name, int):
			instance.fgm_name.arg = 0

	@classmethod
	def write_fields(cls, stream, instance):
		super().write_fields(stream, instance)
		Pointer.to_stream(stream, instance.fgm_name)
		Vector3F.to_stream(stream, instance.vec_0)
		Vector3F.to_stream(stream, instance.vec_1)
		Uint.to_stream(stream, instance.a)
		Uint.to_stream(stream, instance.b)
		Vector3F.to_stream(stream, instance.vec_2)
		Vector3F.to_stream(stream, instance.vec_3)
		Vector3F.to_stream(stream, instance.vec_4)
		Uint.to_stream(stream, instance.c)
		Uint.to_stream(stream, instance.d)
		Float.to_stream(stream, instance.e)
		Float.to_stream(stream, instance.f)
		Uint.to_stream(stream, instance.g)
		Array.to_stream(stream, instance.floats, (39,), Float, instance.context, 0, None)
		Uint.to_stream(stream, instance.d)
		Float.to_stream(stream, instance.e)

	@classmethod
	def _get_filtered_attribute_list(cls, instance):
		yield from super()._get_filtered_attribute_list(instance)
		yield 'fgm_name', Pointer, (0, generated.formats.ovl_base.basic.ZStringObfuscated), (False, None)
		yield 'vec_0', Vector3F, (0, None), (False, None)
		yield 'vec_1', Vector3F, (0, None), (False, None)
		yield 'a', Uint, (0, None), (False, None)
		yield 'b', Uint, (0, None), (False, None)
		yield 'vec_2', Vector3F, (0, None), (False, None)
		yield 'vec_3', Vector3F, (0, None), (False, None)
		yield 'vec_4', Vector3F, (0, None), (False, None)
		yield 'c', Uint, (0, None), (False, None)
		yield 'd', Uint, (0, None), (False, None)
		yield 'e', Float, (0, None), (False, None)
		yield 'f', Float, (0, None), (False, None)
		yield 'g', Uint, (0, None), (False, None)
		yield 'floats', Array, ((39,), Float, 0, None), (False, None)
		yield 'd', Uint, (0, None), (False, None)
		yield 'e', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'DinoEffectsHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self, indent=0):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* fgm_name = {self.fmt_member(self.fgm_name, indent+1)}'
		s += f'\n	* vec_0 = {self.fmt_member(self.vec_0, indent+1)}'
		s += f'\n	* vec_1 = {self.fmt_member(self.vec_1, indent+1)}'
		s += f'\n	* a = {self.fmt_member(self.a, indent+1)}'
		s += f'\n	* b = {self.fmt_member(self.b, indent+1)}'
		s += f'\n	* vec_2 = {self.fmt_member(self.vec_2, indent+1)}'
		s += f'\n	* vec_3 = {self.fmt_member(self.vec_3, indent+1)}'
		s += f'\n	* vec_4 = {self.fmt_member(self.vec_4, indent+1)}'
		s += f'\n	* c = {self.fmt_member(self.c, indent+1)}'
		s += f'\n	* d = {self.fmt_member(self.d, indent+1)}'
		s += f'\n	* e = {self.fmt_member(self.e, indent+1)}'
		s += f'\n	* f = {self.fmt_member(self.f, indent+1)}'
		s += f'\n	* g = {self.fmt_member(self.g, indent+1)}'
		s += f'\n	* floats = {self.fmt_member(self.floats, indent+1)}'
		s += f'\n	* d = {self.fmt_member(self.d, indent+1)}'
		s += f'\n	* e = {self.fmt_member(self.e, indent+1)}'
		return s

	def __repr__(self, indent=0):
		s = self.get_info_str(indent)
		s += self.get_fields_str(indent)
		s += '\n'
		return s
