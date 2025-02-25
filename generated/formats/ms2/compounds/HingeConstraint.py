from generated.formats.ms2.compounds.Constraint import Constraint
from generated.formats.ms2.imports import name_type_map


class HingeConstraint(Constraint):

	"""
	fPhysicsHingeJoint
	used in JWE dinos
	no longer used in PZ, JWE2
	"""

	__name__ = 'HingeConstraint'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# normalized direction of Z axis in blender
		self.direction = name_type_map['Vector3'](self.context, 0, None)

		# radians
		self.limits = name_type_map['RotationRange'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'direction', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'limits', name_type_map['RotationRange'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'direction', name_type_map['Vector3'], (0, None), (False, None)
		yield 'limits', name_type_map['RotationRange'], (0, None), (False, None)
