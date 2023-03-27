from generated.formats.base.basic import Float
from generated.formats.ms2.compounds.Constraint import Constraint
from generated.formats.ms2.compounds.Vector3 import Vector3


class StretchConstraint(Constraint):

	"""
	used in JWE1 dinos
	no longer used in PZ, JWE2
	"""

	__name__ = 'StretchConstraint'

	_import_key = 'ms2.compounds.StretchConstraint'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# location of the joint
		self.loc = Vector3(self.context, 0, None)

		# normalized
		self.direction = Vector3(self.context, 0, None)

		# min, le 0
		self.min = 0.0

		# max, ge 0
		self.max = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('loc', Vector3, (0, None), (False, None), None)
		yield ('direction', Vector3, (0, None), (False, None), None)
		yield ('min', Float, (0, None), (False, None), None)
		yield ('max', Float, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'loc', Vector3, (0, None), (False, None)
		yield 'direction', Vector3, (0, None), (False, None)
		yield 'min', Float, (0, None), (False, None)
		yield 'max', Float, (0, None), (False, None)


StretchConstraint.init_attributes()
