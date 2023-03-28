import numpy
from generated.array import Array
from generated.base_struct import BaseStruct
from generated.formats.base.basic import Uint
from generated.formats.ms2.compounds.Matrix33 import Matrix33
from generated.formats.ms2.compounds.Vector3 import Vector3


class BoundingBox(BaseStruct):

	__name__ = 'BoundingBox'

	_import_key = 'ms2.compounds.BoundingBox'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.rotation = Matrix33(self.context, 0, None)

		# center of the box
		self.center = Vector3(self.context, 0, None)

		# total width
		self.extent = Vector3(self.context, 0, None)

		# probably padding
		self.zeros = Array(self.context, 0, None, (0,), Uint)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('rotation', Matrix33, (0, None), (False, None), (None, None))
		yield ('center', Vector3, (0, None), (False, None), (None, None))
		yield ('extent', Vector3, (0, None), (False, None), (None, None))
		yield ('zeros', Array, (0, None, (3,), Uint), (False, None), (lambda context: context.version == 32, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'rotation', Matrix33, (0, None), (False, None)
		yield 'center', Vector3, (0, None), (False, None)
		yield 'extent', Vector3, (0, None), (False, None)
		if instance.context.version == 32:
			yield 'zeros', Array, (0, None, (3,), Uint), (False, None)


BoundingBox.init_attributes()
