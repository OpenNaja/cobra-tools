from generated.base_struct import BaseStruct
from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.ms2.compounds.Vector3 import Vector3


class RigidBody(BaseStruct):

	__name__ = 'RigidBody'

	_import_key = 'ms2.compounds.RigidBody'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)

		# 2 kinematic, 0 1 static
		self.flag = 0

		# center of mass - from the head of the bone the collider is attached to
		self.loc = Vector3(self.context, 0, None)

		# mass of joint or object
		self.mass = 0.0

		# coefficient of static friction(small wants to roll, larger wants to slide)
		self.static_friction = 0.0

		# 2.0 in unk1 makes the object not to stop ever, it is breakdancing
		self.unk_1 = 0.0

		# Related to Bounciness
		self.unk_2 = 0.0

		# NOT air resistance
		self.unknown_friction = 0.0

		# ?
		self.unk_4 = 0.0

		# coefficient of dynamic friction
		self.dynamic_friction = 0.0
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield ('flag', Uint, (0, None), (False, None), None)
		yield ('loc', Vector3, (0, None), (False, None), None)
		yield ('mass', Float, (0, None), (False, None), None)
		yield ('static_friction', Float, (0, None), (False, None), None)
		yield ('unk_1', Float, (0, None), (False, None), None)
		yield ('unk_2', Float, (0, None), (False, None), None)
		yield ('unknown_friction', Float, (0, None), (False, None), None)
		yield ('unk_4', Float, (0, None), (False, None), None)
		yield ('dynamic_friction', Float, (0, None), (False, None), None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'flag', Uint, (0, None), (False, None)
		yield 'loc', Vector3, (0, None), (False, None)
		yield 'mass', Float, (0, None), (False, None)
		yield 'static_friction', Float, (0, None), (False, None)
		yield 'unk_1', Float, (0, None), (False, None)
		yield 'unk_2', Float, (0, None), (False, None)
		yield 'unknown_friction', Float, (0, None), (False, None)
		yield 'unk_4', Float, (0, None), (False, None)
		yield 'dynamic_friction', Float, (0, None), (False, None)


RigidBody.init_attributes()
