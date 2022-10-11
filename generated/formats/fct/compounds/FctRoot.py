from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Int
from generated.formats.base.basic import Short
from generated.formats.base.basic import Uint64
from generated.formats.fct.compounds.Font import Font
from generated.formats.ovl_base.compounds.MemStruct import MemStruct


class FctRoot(MemStruct):

	"""
	JWE1: 104 bytes
	"""

	__name__ = 'FctRoot'

	_import_key = 'fct.compounds.FctRoot'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
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
		self.fonts = Array(self.context, 0, None, (0,), Font)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('u_0', Short, (0, None), (False, None), None),
		('u_1', Short, (0, None), (False, None), None),
		('a', Float, (0, None), (False, None), None),
		('b', Float, (0, None), (False, None), None),
		('c', Float, (0, None), (False, None), None),
		('minus_1', Short, (0, None), (False, None), None),
		('z_0', Short, (0, None), (False, None), None),
		('z_1', Int, (0, None), (False, None), None),
		('z_2', Uint64, (0, None), (False, None), None),
		('offset', Uint64, (0, None), (False, None), None),
		('fonts', Array, (0, None, (4,), Font), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'u_0', Short, (0, None), (False, None)
		yield 'u_1', Short, (0, None), (False, None)
		yield 'a', Float, (0, None), (False, None)
		yield 'b', Float, (0, None), (False, None)
		yield 'c', Float, (0, None), (False, None)
		yield 'minus_1', Short, (0, None), (False, None)
		yield 'z_0', Short, (0, None), (False, None)
		yield 'z_1', Int, (0, None), (False, None)
		yield 'z_2', Uint64, (0, None), (False, None)
		yield 'offset', Uint64, (0, None), (False, None)
		yield 'fonts', Array, (0, None, (4,), Font), (False, None)
