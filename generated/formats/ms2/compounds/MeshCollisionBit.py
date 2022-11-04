import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Ushort


class MeshCollisionBit(BaseStruct):

	__name__ = 'MeshCollisionBit'

	_import_key = 'ms2.compounds.MeshCollisionBit'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# ?
		self.countd = Array(self.context, 0, None, (0,), Ushort)

		# always 2954754766?
		self.consts = Array(self.context, 0, None, (0,), Uint)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('countd', Array, (0, None, (34,), Ushort), (False, None), None),
		('consts', Array, (0, None, (3,), Uint), (False, None), None),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'countd', Array, (0, None, (34,), Ushort), (False, None)
		yield 'consts', Array, (0, None, (3,), Uint), (False, None)
