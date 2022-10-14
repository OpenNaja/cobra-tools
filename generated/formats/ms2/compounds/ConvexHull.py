import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.ms2.compounds.Matrix33 import Matrix33
from generated.formats.ms2.compounds.Vector3 import Vector3


class ConvexHull(BaseStruct):

	__name__ = 'ConvexHull'

	_import_key = 'ms2.compounds.ConvexHull'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 16 for anubis: 4 hulls * 16 * 12 (size of vert)
		self.vertex_count = 0
		self.rotation = Matrix33(self.context, 0, None)

		# center of the box
		self.offset = Vector3(self.context, 0, None)

		# probably padding
		self.zeros = Array(self.context, 0, None, (0,), Uint)
		if set_default:
			self.set_defaults()

	_attribute_list = BaseStruct._attribute_list + [
		('vertex_count', Uint, (0, None), (False, None), None),
		('rotation', Matrix33, (0, None), (False, None), None),
		('offset', Vector3, (0, None), (False, None), None),
		('zeros', Array, (0, None, (5,), Uint), (False, None), True),
		('zeros', Array, (0, None, (2,), Uint), (False, None), True),
		]

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'vertex_count', Uint, (0, None), (False, None)
		yield 'rotation', Matrix33, (0, None), (False, None)
		yield 'offset', Vector3, (0, None), (False, None)
		if instance.context.version == 32:
			yield 'zeros', Array, (0, None, (5,), Uint), (False, None)
		if instance.context.version >= 48:
			yield 'zeros', Array, (0, None, (2,), Uint), (False, None)
