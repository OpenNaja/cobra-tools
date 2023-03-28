from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.ms2.compounds.Vector3 import Vector3
from generated.formats.ms2.compounds.Vector4 import Vector4


class Bone(BaseStruct):

	"""
	32 bytes
	bones, rot first
	"""

	__name__ = 'Bone'

	_import_key = 'ms2.compounds.Bone'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.loc = Vector3(self.context, 0, None)
		self.scale = 0.0
		self.rot = Vector4(self.context, 0, None)
		self.loc = Vector3(self.context, 0, None)
		self.scale = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('loc', Vector3, (0, None), (False, None), True)
		yield ('scale', Float, (0, None), (False, None), True)
		yield ('rot', Vector4, (0, None), (False, None), True)
		yield ('rot', Vector4, (0, None), (False, None), True)
		yield ('loc', Vector3, (0, None), (False, None), True)
		yield ('scale', Float, (0, None), (False, None), True)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		if instance.context.version <= 47:
			yield 'loc', Vector3, (0, None), (False, None)
			yield 'scale', Float, (0, None), (False, None)
			yield 'rot', Vector4, (0, None), (False, None)
		if instance.context.version >= 48:
			yield 'rot', Vector4, (0, None), (False, None)
			yield 'loc', Vector3, (0, None), (False, None)
			yield 'scale', Float, (0, None), (False, None)

	def set_bone(self, matrix):
		pos, quat, sca = matrix.decompose()
		self.loc.x, self.loc.y, self.loc.z = pos.x, pos.y, pos.z
		self.rot.x, self.rot.y, self.rot.z, self.rot.w = quat.x, quat.y, quat.z, quat.w
		self.scale = sca.x



Bone.init_attributes()
