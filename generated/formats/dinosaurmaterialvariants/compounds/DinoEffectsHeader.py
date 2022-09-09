import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.dinosaurmaterialvariants.compounds.Vector3F import Vector3F
from generated.formats.ovl_base.basic import ZStringObfuscated
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class DinoEffectsHeader(MemStruct):

	__name__ = 'DinoEffectsHeader'

	_import_path = 'generated.formats.dinosaurmaterialvariants.compounds.DinoEffectsHeader'

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
		self.floats = Array(self.context, 0, None, (0,), Float)
		self.d = 0
		self.e = 0.0
		self.fgm_name = Pointer(self.context, 0, ZStringObfuscated)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'fgm_name', Pointer, (0, ZStringObfuscated), (False, None)
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
		yield 'floats', Array, (0, None, (39,), Float), (False, None)
		yield 'd', Uint, (0, None), (False, None)
		yield 'e', Float, (0, None), (False, None)

	def get_info_str(self, indent=0):
		return f'DinoEffectsHeader [Size: {self.io_size}, Address: {self.io_start}] {self.name}'
