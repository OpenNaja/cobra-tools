from generated.formats.ms2.compounds.Constraint import Constraint


class BallConstraint(Constraint):

	"""
	fPhysicsBallJoint
	used in JWE Pteranodon
	no longer used in PZ, JWE2
	"""

	__name__ = 'BallConstraint'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
