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

	_import_key = 'dinosaurmaterialvariants.compounds.DinoEffectsHeader'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.vec_0 = Vector3F(self.context, 0, None)
		self.vec_1 = Vector3F(self.context, 0, None)
		self.a = 0
		self.b = 0
		self.vec_2 = Vector3F(self.context, 0, None)
		self.vec_3 = Vector3F(self.context, 0, None)
		self.vec_4 = Vector3F(self.context, 0, None)
		self.vec_5 = Vector3F(self.context, 0, None)
		self.c = 0
		self.d = 0
		self.floats_1 = Array(self.context, 0, None, (0,), Float)
		self.e = 0
		self.floats_2 = Array(self.context, 0, None, (0,), Float)
		self.f = 0
		self.floats_3 = Array(self.context, 0, None, (0,), Float)
		self.g = 0
		self.floats_4 = Array(self.context, 0, None, (0,), Float)
		self.h = 0
		self.floats_5 = Array(self.context, 0, None, (0,), Float)
		self.i = 0
		self.float = 0.0
		self.fgm_name = Pointer(self.context, 0, ZStringObfuscated)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('fgm_name', Pointer, (0, ZStringObfuscated), (False, None), None),
		('vec_0', Vector3F, (0, None), (False, None), None),
		('vec_1', Vector3F, (0, None), (False, None), None),
		('a', Uint, (0, None), (False, None), None),
		('b', Uint, (0, None), (False, None), None),
		('vec_2', Vector3F, (0, None), (False, None), None),
		('vec_3', Vector3F, (0, None), (False, None), None),
		('vec_4', Vector3F, (0, None), (False, None), None),
		('vec_5', Vector3F, (0, None), (False, None), None),
		('c', Uint, (0, None), (False, None), None),
		('d', Uint, (0, None), (False, None), None),
		('floats_1', Array, (0, None, (2,), Float), (False, None), None),
		('e', Uint, (0, None), (False, None), None),
		('floats_2', Array, (0, None, (2,), Float), (False, None), None),
		('f', Uint, (0, None), (False, None), None),
		('floats_3', Array, (0, None, (8,), Float), (False, None), None),
		('g', Uint, (0, None), (False, None), None),
		('floats_4', Array, (0, None, (6,), Float), (False, None), None),
		('h', Uint, (0, None), (False, None), None),
		('floats_5', Array, (0, None, (20,), Float), (False, None), None),
		('i', Uint, (0, None), (False, None), None),
		('float', Float, (0, None), (False, None), None),
		]

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
		yield 'vec_5', Vector3F, (0, None), (False, None)
		yield 'c', Uint, (0, None), (False, None)
		yield 'd', Uint, (0, None), (False, None)
		yield 'floats_1', Array, (0, None, (2,), Float), (False, None)
		yield 'e', Uint, (0, None), (False, None)
		yield 'floats_2', Array, (0, None, (2,), Float), (False, None)
		yield 'f', Uint, (0, None), (False, None)
		yield 'floats_3', Array, (0, None, (8,), Float), (False, None)
		yield 'g', Uint, (0, None), (False, None)
		yield 'floats_4', Array, (0, None, (6,), Float), (False, None)
		yield 'h', Uint, (0, None), (False, None)
		yield 'floats_5', Array, (0, None, (20,), Float), (False, None)
		yield 'i', Uint, (0, None), (False, None)
		yield 'float', Float, (0, None), (False, None)
