import numpy
from generated.array import Array
from generated.formats.base.basic import Float
from generated.formats.base.basic import Int
from generated.formats.base.basic import Ubyte
from generated.formats.base.basic import Uint
from generated.formats.ovl_base.basic import Bool
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.renderparameters.compounds.ZStrPtr import ZStrPtr


class ParamData(MemStruct):

	"""
	16 bytes
	"""

	__name__ = 'ParamData'

	_import_key = 'renderparameters.compounds.ParamData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.data = Array(self.context, 0, None, (0,), ZStrPtr)
		if set_default:
			self.set_defaults()

	_attribute_list = MemStruct._attribute_list + [
		('data', Array, (0, None, (1,), Bool), (False, None), True),
		('data', Array, (0, None, (1,), Float), (False, None), True),
		('data', Array, (0, None, (1,), Int), (False, None), True),
		('data', Array, (0, None, (1,), Uint), (False, None), True),
		('data', Array, (0, None, (2,), Float), (False, None), True),
		('data', Array, (0, None, (3,), Float), (False, None), True),
		('data', Array, (0, None, (4,), Float), (False, None), True),
		('data', Array, (0, None, (4,), Ubyte), (False, None), True),
		('data', Array, (0, None, (4,), Float), (False, None), True),
		('data', Array, (0, None, (1,), ZStrPtr), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.arg == 0:
			yield 'data', Array, (0, None, (1,), Bool), (False, None)
		if instance.arg == 1:
			yield 'data', Array, (0, None, (1,), Float), (False, None)
		if instance.arg == 2:
			yield 'data', Array, (0, None, (1,), Int), (False, None)
		if instance.arg == 3:
			yield 'data', Array, (0, None, (1,), Uint), (False, None)
		if instance.arg == 4:
			yield 'data', Array, (0, None, (2,), Float), (False, None)
		if instance.arg == 5:
			yield 'data', Array, (0, None, (3,), Float), (False, None)
		if instance.arg == 6:
			yield 'data', Array, (0, None, (4,), Float), (False, None)
		if instance.arg == 7:
			yield 'data', Array, (0, None, (4,), Ubyte), (False, None)
		if instance.arg == 8:
			yield 'data', Array, (0, None, (4,), Float), (False, None)
		if instance.arg == 9:
			yield 'data', Array, (0, None, (1,), ZStrPtr), (False, None)
