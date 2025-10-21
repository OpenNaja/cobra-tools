from generated.base_struct import BaseStruct
from generated.formats.ms2.imports import name_type_map


class RigidBody(BaseStruct):

	__name__ = 'RigidBody'


	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.flag = name_type_map['RigidBodyFlag'](self.context, 0, None)

		# center of mass - relative to joint
		self.loc = name_type_map['Vector3'](self.context, 0, None)

		# mass of joint or object
		self.mass = name_type_map['Float'](self.context, 0, None)
		self.air_resistance_x = name_type_map['Float'](self.context, 0, None)

		# 2.0 in unk1 makes the object not to stop ever, it is breakdancing
		self.unk_1 = name_type_map['Float'](self.context, 0, None)

		# Related to Bounciness
		self.unk_2 = name_type_map['Float'](self.context, 0, None)
		self.air_resistance_y = name_type_map['Float'](self.context, 0, None)

		# ?
		self.unk_4 = name_type_map['Float'](self.context, 0, None)
		self.air_resistance_z = name_type_map['Float'](self.context, 0, None)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_attribute_list(cls):
		yield from super()._get_attribute_list()
		yield 'flag', name_type_map['RigidBodyFlag'], (0, None), (False, None), (None, None)
		yield 'loc', name_type_map['Vector3'], (0, None), (False, None), (None, None)
		yield 'mass', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'air_resistance_x', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_1', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_2', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'air_resistance_y', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'unk_4', name_type_map['Float'], (0, None), (False, None), (None, None)
		yield 'air_resistance_z', name_type_map['Float'], (0, None), (False, None), (None, None)

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'flag', name_type_map['RigidBodyFlag'], (0, None), (False, None)
		yield 'loc', name_type_map['Vector3'], (0, None), (False, None)
		yield 'mass', name_type_map['Float'], (0, None), (False, None)
		yield 'air_resistance_x', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_1', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_2', name_type_map['Float'], (0, None), (False, None)
		yield 'air_resistance_y', name_type_map['Float'], (0, None), (False, None)
		yield 'unk_4', name_type_map['Float'], (0, None), (False, None)
		yield 'air_resistance_z', name_type_map['Float'], (0, None), (False, None)
