from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float


class Vector3(BaseStruct):

	"""
	A vector in 3D space (x,y,z).
	"""

	__name__ = 'Vector3'

	_import_key = 'ms2.compounds.Vector3'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# First coordinate.
		self.x = 0.0

		# Second coordinate.
		self.y = 0.0

		# Third coordinate.
		self.z = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('x', Float, (0, None), (False, None), (None, None))
		yield ('y', Float, (0, None), (False, None), (None, None))
		yield ('z', Float, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'x', Float, (0, None), (False, None)
		yield 'y', Float, (0, None), (False, None)
		yield 'z', Float, (0, None), (False, None)

	def set(self, vec):
		if hasattr(vec, "x"):
			self.x = vec.x
			self.y = vec.y
			self.z = vec.z
		else:
			self.x, self.y, self.z = vec

	def __repr__(self):
		return f"[ {self.x:6.3f} {self.y:6.3f} {self.z:6.3f} ]"



Vector3.init_attributes()
