from generated.base_struct import BaseStruct
from generated.formats.ms2.compounds.Matrix33 import Matrix33
from generated.formats.ms2.compounds.Vector3 import Vector3


class JointTransform(BaseStruct):

	"""
	Describes a joint in armature space.
	"""

	__name__ = 'JointTransform'

	_import_key = 'ms2.compounds.JointTransform'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# the rotation of the joint, inverted
		self.rot = Matrix33(self.context, 0, None)

		# the location of the joint
		self.loc = Vector3(self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('rot', Matrix33, (0, None), (False, None), (None, None))
		yield ('loc', Vector3, (0, None), (False, None), (None, None))

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'rot', Matrix33, (0, None), (False, None)
		yield 'loc', Vector3, (0, None), (False, None)
