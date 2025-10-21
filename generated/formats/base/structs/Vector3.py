from generated.base_struct import BaseStruct
from generated.formats.base.imports import name_type_map


class Vector3(BaseStruct):

	"""
	A vector in 3D space (x,y,z).
	"""

	__name__ = 'Vector3'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# First coordinate.
		self.x = name_type_map['Float'](self.context, 0, None)

		# Second coordinate.
		self.y = name_type_map['Float'](self.context, 0, None)

		# Third coordinate.
		self.z = name_type_map['Float'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'x', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'y', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'z', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'x', name_type_map['Float'], (0, None), (False, None)
		yield 'y', name_type_map['Float'], (0, None), (False, None)
		yield 'z', name_type_map['Float'], (0, None), (False, None)

	def __setitem__(self, k, v):
		self.x, self.y, self.z = v

	def set(self, vec):
		if hasattr(vec, "x"):
			self.x = vec.x
			self.y = vec.y
			self.z = vec.z
		else:
			self.x, self.y, self.z = vec

	@staticmethod
	def format_indented(self, indent=0):
		return f"[ {self.x:6.3f} {self.y:6.3f} {self.z:6.3f} ]"

	def __eq__(self, other):
		if hasattr(other, "x"):
			return self.x == other.x and self.y == other.y and self.z == other.z

	def __mul__(self, other):
		if isinstance(other, float):
			self.x *= other
			self.y *= other
			self.z *= other
			return self
		else:
			raise NotImplementedError(f"can't mul Vector3 * {type(other)}")

	def __imul__(self, other):
		return self * other

