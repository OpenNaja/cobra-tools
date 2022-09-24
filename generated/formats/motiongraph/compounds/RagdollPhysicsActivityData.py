from generated.formats.base.basic import Float
from generated.formats.base.basic import Uint
from generated.formats.base.basic import Uint64
from generated.formats.base.basic import ZString
from generated.formats.motiongraph.bitstructs.RagdollPhysicsActivityFlags import RagdollPhysicsActivityFlags
from generated.formats.ovl_base.compounds.MemStruct import MemStruct
from generated.formats.ovl_base.compounds.Pointer import Pointer


class RagdollPhysicsActivityData(MemStruct):

	"""
	? bytes
	"""

	__name__ = 'RagdollPhysicsActivityData'

	_import_key = 'motiongraph.compounds.RagdollPhysicsActivityData'

	def __init__(self, context, arg=0, template=None, set_default=True):
		super().__init__(context, arg, template, set_default=False)
		self.flag = RagdollPhysicsActivityFlags(self.context, 0, None)
		self._flag_pad = 0
		self.collision_exclude_mask = 0
		self.min_motor_driving_force = 0.0
		self.max_motor_driving_force = 0.0
		self.pose_match_lin_threshold = 0.0
		self.pose_match_ang_threshold = 0.0
		self.bone_chain_priority = 0
		self.root_bone_name = Pointer(self.context, 0, ZString)
		self.collision_exclude_0 = Pointer(self.context, 0, ZString)
		self.collision_exclude_1 = Pointer(self.context, 0, ZString)
		self.collision_exclude_2 = Pointer(self.context, 0, ZString)
		self.collision_exclude_3 = Pointer(self.context, 0, ZString)
		self.collision_exclude_4 = Pointer(self.context, 0, ZString)
		self.collision_exclude_5 = Pointer(self.context, 0, ZString)
		self.collision_exclude_6 = Pointer(self.context, 0, ZString)
		self.collision_exclude_7 = Pointer(self.context, 0, ZString)
		self.motor_weight_variable = Pointer(self.context, 0, ZString)
		self.data_stream_name = Pointer(self.context, 0, ZString)
		self.data_stream_type = Pointer(self.context, 0, ZString)
		if set_default:
			self.set_defaults()

	@classmethod
	def _get_filtered_attribute_list(cls, instance, include_abstract=True):
		yield from super()._get_filtered_attribute_list(instance, include_abstract)
		yield 'flag', RagdollPhysicsActivityFlags, (0, None), (False, None)
		yield '_flag_pad', Uint, (0, None), (False, None)
		yield 'root_bone_name', Pointer, (0, ZString), (False, None)
		yield 'collision_exclude_mask', Uint64, (0, None), (False, None)
		yield 'collision_exclude_0', Pointer, (0, ZString), (False, None)
		yield 'collision_exclude_1', Pointer, (0, ZString), (False, None)
		yield 'collision_exclude_2', Pointer, (0, ZString), (False, None)
		yield 'collision_exclude_3', Pointer, (0, ZString), (False, None)
		yield 'collision_exclude_4', Pointer, (0, ZString), (False, None)
		yield 'collision_exclude_5', Pointer, (0, ZString), (False, None)
		yield 'collision_exclude_6', Pointer, (0, ZString), (False, None)
		yield 'collision_exclude_7', Pointer, (0, ZString), (False, None)
		yield 'min_motor_driving_force', Float, (0, None), (False, None)
		yield 'max_motor_driving_force', Float, (0, None), (False, None)
		yield 'motor_weight_variable', Pointer, (0, ZString), (False, None)
		yield 'pose_match_lin_threshold', Float, (0, None), (False, None)
		yield 'pose_match_ang_threshold', Float, (0, None), (False, None)
		yield 'bone_chain_priority', Uint64, (0, None), (False, None)
		yield 'data_stream_name', Pointer, (0, ZString), (False, None)
		yield 'data_stream_type', Pointer, (0, ZString), (False, None)
